from conans import ConanFile, tools
import os
import multiprocessing


class LibGpsConan(ConanFile):
    name = "libgps"
    version = "3.21"
    license = "BSD-2-Clause"
    author = "matt@woelfware.com"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "A service daemon that monitors one or more GNSS (GPS) or AIS receivers attached to a host computer through serial or USB ports."
    topics = ("gps")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = {"shared": False}
    generators = "pkg_config"

    def source(self):
        git = tools.Git(folder="gpsd")
        git.clone("https://gitlab.com/gpsd/gpsd.git", "release-{}".format(LibGpsConan.version))

    def build(self):
        debug_opts = ['-Q', 'debug=1'] if self.settings.build_type == 'Debug' else []
        os.makedirs("build")
        with tools.chdir("build"):
            self.run(['scons', '-j', '{}'.format(multiprocessing.cpu_count()), '-C', '{}/gpsd'.format(self.source_folder)] + debug_opts)

    def package(self):
        self.copy("*.h", dst="include", src="gpsd")
        self.copy("*.dll", dst="lib", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["libgps"]

