# Gather info about installed and available snaps to generate lists.

import gi
import os
import pwd
import subprocess

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from pathlib import Path

import snapctl


class InstalledSnapRow(Gtk.ListBoxRow):
    def __init__(self, data):
        super(Gtk.ListBoxRow, self).__init__()
        self.data = data

        # Parse the input data.
        icon = data['icon']
        snap = data['name']
        description = data['summary']
        rev_installed = data['revision']
        rev_available = 'N/A'
        note = 'revision ' + rev_installed + ' -> ' + rev_available
        flag = data['confinement']

        # Define the row.
        box_row = Gtk.Box(orientation='horizontal')
        self.add(box_row)

        # Define the various parts of the row box.
        label_icon = Gtk.Image.new_from_file(icon)
        box_info = Gtk.Box(orientation='vertical')
        #label_rev_installed = Gtk.Label(rev_installed)
        #label_rev_available = Gtk.Label(rev_available)
        label_update_note = Gtk.Label(note)

        # Pack the various parts of the row box.
        box_row.pack_start(label_icon, False, False, 5)
        box_row.pack_start(box_info, False, False, 5)
        #box_row.pack_end(label_rev_installed, False, False, 5)
        #box_row.pack_end(label_rev_available, False, False, 5)
        box_row.pack_end(label_update_note, False, False, 5)

        # Define the 2 parts of the info box within the row.
        label_name = Gtk.Label(snap)
        label_name.set_alignment(0.0, 0.5)
        label_name.set_markup("<span weight=\"bold\">" + snap + "</span>")
        label_description = Gtk.Label(description)
        label_description.set_alignment(0.0, 0.5)

        # Pack the 2 parts of the info box into the row box.
        box_info.pack_start(label_name, False, False, 1)
        box_info.pack_start(label_description, False, False, 1)


def populate_listbox(list_box, contents_dict):
    rows = {}
    count = 0
    for snap in sorted(contents_dict.keys()):
        row = InstalledSnapRow(contents_dict[snap])
        list_box.add(row)
        rows[snap] = count
        count += 1
    return rows

def guess_offline_source_folder():
    user = pwd.getpwuid(int(os.environ['PKEXEC_UID'])).pw_name
    # Check for USB device wasta-offline folder.
    try:
        begin = sorted(Path('/media/' + user).glob('*/wasta-offline'))[0]
    except IndexError:
        try:
            # Check /mnt. How deep could it be, though?
            begin = sorted(Path('/mnt').glob('wasta-offline'))[0]
        except IndexError:
            try:
                # Check for VBox shared wasta-offline folder.
                begin = sorted(Path('/media/').glob('*/wasta-offline'))[0]
            except IndexError:
                # As a last resort just choose $HOME.
                begin = Path('/home/' + user)
    return begin.as_posix()