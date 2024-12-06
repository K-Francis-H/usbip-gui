project('usbip-gui')

python = import('python').find_installation('python', modules: ['tkinter'])
python.dependency()


subdir('po')

sources = ['./usbip-gui/__init__.py', './usbip-gui/__main__.py', './usbip-gui/main.py', './usbip-gui/gui.py']

launch_data = configuration_data({
    'MAIN_FILE_PATH': join_paths(python.get_install_dir(), meson.project_name(), 'main.py')
})

desktop_file = configure_file(
    input: './share/usbip-gui.desktop',
    configuration: launch_data,
    output: 'usbip-gui.desktop'
)

install_data(desktop_file, install_dir: '/usr/share/applications/')
python.install_sources(sources, subdir: meson.project_name())
