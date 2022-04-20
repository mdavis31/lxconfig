# lxconfig
A group of configuration settings, scripts and more for my various used linux distros.

---

### MGD Folder Standard v1
- $HOME folder:
  - Used for any personal projects/documents being worked on
  - This whole directory should be backed up
  - Keep the folders in there with capitals and add:
    - /Apps - application builds not done in package manager
    - /Dev - development projects
    - /Games - *(optional) You can also put games in stuff
    - /Security - Any secrets/keys that need stored

- /stuff folder:
  - Sits at the root directory, used for bulk storage
  - Will typically be mounted to another drive
  - Use permissions (2775) and wheel/other group
  - Add the following subfolders:
    - /archive - old projects/documents not needed day-to-day
    - /backups - backup data for all devices (including own $HOME)
    - /drive   - google drive
    - /media/documents
    - /media/music
    - /media/pictures
    - /media/videos
    - /media/games *(optional)

### Fedora
- rpm fusion?