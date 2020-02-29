'''
Animagrad (AMG)
(c) 2018

date: 23/10/2018
modified: 04/12/2018 20:09:07

Author: Yuri Meshalkin
e-mail: yuri.meshalkin@animagrad.com
Author: Andrey Babak
e-mail: ababak@gmail.com
------------------------------
description: Maya XGEN export
------------------------------
'''

__version__ = '1.0.1'

import sys
import os
import re
import time
import tempfile
import shutil
import maya.cmds as cmds
import maya.mel as mel
import xgenm as xg 
import xgenm.xgGlobal as xgg

from amg.system import navigator

amg_modules = '//bstorage/rep/set/scripts'
if amg_modules not in sys.path:
    sys.path.append(amg_modules)
from amg.system import cpp


def _xgen_export_bgeo(bgeo_out_dir, descr, palette, frame_range, padding=4):
    '''
    Exports given description to .bgeo for frame range (start,end)
    Returns a list of assets used as primitives
    e.g. [ 'RubberToy', 'PigHead', 'Archive' ]
    '''

    print '* _xgen_export_bgeo...'
    obj_list = []
    # descr_name = re.sub(r'_description[\d]*$', '', descr)
    try:
        xg.setActive(palette, descr, 'ParticleRenderer')
    except RuntimeError as e:
        print ' ParticleRenderer not available'
        print ' Error:', e
        return []
    files = xg.getAttr('files', palette, descr, 'ArchivePrimitive')
    # from "files" string find ArchiveGroup number and name
    # e.g. [('0', 'RubberToy'), ('1', 'PigHead'), ('2', 'Archive')]
    groups = re.findall(r'#ArchiveGroup (\d) name="(\D+)" thumbnail', files)
    archives_dict = dict(groups)
    for id in sorted(archives_dict):
        obj_list.append(str(archives_dict[id]))

    for frame in frame_range:
        cmds.currentTime(frame)
        suffix = '.{0:{fill}{width}{base}}.bgeo'.format(
            frame, fill='0', base='d', width=padding)
        bgeo_path = bgeo_out_dir + '/' + descr + suffix
        xg.setAttr('particleFile', bgeo_path, palette, descr, 'ParticleRenderer')
        print '  Exporting... ' + bgeo_path
        mel.eval('xgmParticleRender {"' + descr + '"};')
    return obj_list

def _abc_from_bgeo(bgeo_out_dir,
                   abc_file,
                   descr,
                   obj_list,
                   frame_range, 
                   padding=4):
    '''
    Generates alembic archive for points and archives
    from xgen descriptions
    '''
    
    print '* _abc_from_bgeo...'
    # do nothing if obj_list is empty
    if not obj_list:
        return
    descr_name = re.sub(r'_description[\d]*$', '', descr)
    bgeo_cpp = cpp.call(str(bgeo_out_dir), str(abc_file), str(descr_name),
                obj_list, lib='write_alembic', func="bgeo2abc")
    

def export(scene_path='', frame_range=None):
    '''
    Export XGEN descriptions to alembic
    '''

    print '* Start exporting XGen descriptions to .bgeo...'

    if (cmds.getAttr("defaultRenderGlobals.animation")):
        print "Animation on"
        f_start = int(cmds.playbackOptions(query=True, min=True))
        f_end = int(cmds.playbackOptions(query=True, max=True)) + 1
        frame_range = range(f_start,f_end)
    else:
        print "Animation off"
        frame = int(cmds.currentTime(query=True))
        frame_range = [frame]
    
    tmp_dir = tempfile.mkdtemp()
    print 'tmp_dir =', tmp_dir

    scene_path = scene_path or cmds.file(query=True, list=True)[0]
    fields = navigator.fields_from_path(scene_path)
    print 'fields =', fields
    if not fields:
        print '[ERROR] Scene path not recognized: ' + scene_path
        return

    palettes = xg.palettes()
    for palette in palettes:
        # Get descriptions (full name) of each collection
        descriptions = list(xg.descriptions(palette))
        for descr in descriptions:
            if 'ArchivePrimitive' in xg.objects(palette, descr, True):
                # descr_name = re.sub(r'_description[\d]*$', '', descr)
                abc_path = navigator.path_from_fields(
                    fields,
                    data_type='cache_scatter',
                    update={
                        'group': descr.encode('ascii'),
                    })
                print 'abc_path =', abc_path
                if not os.path.isdir(os.path.dirname(abc_path)):
                    os.makedirs(os.path.dirname(abc_path))
                # export .bgeo sequence for current description
                # and store archive primitives names to "obj_list"
                obj_list = _xgen_export_bgeo(
                    tmp_dir, 
                    descr, 
                    palette, 
                    frame_range)
                # read .bgeo sequence and save animated array
                # of tansforms matrices for each primitive from "obj_list"
                # to alembic file "abc_path"
                _abc_from_bgeo(
                    tmp_dir, 
                    abc_path, 
                    descr, 
                    obj_list, 
                    frame_range)

    print 'removing tmp_dir =', tmp_dir
    shutil.rmtree(tmp_dir)

    de = xgg.DescriptionEditor  # Get the description editor first.
    de.refresh('Full')  # Do a full UI refresh
    print 'Done'


def main():

    export()


if __name__ == '__main__':
    main()
