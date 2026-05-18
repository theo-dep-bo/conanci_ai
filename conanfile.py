import os
import re
from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMakeDeps, CMake, cmake_layout
from conan.tools.files import load
from conan.tools.scm import Git


class aiRecipe(ConanFile):
    name = "ai"
    requires = "mathlib/[>=1.0 <2]"

    def set_version(self):
        content = load(self, os.path.join(self.recipe_folder, "CMakeLists.txt"))
        version = re.search(r"project\([^)]*VERSION\s+([\d.]+)", content)
        self.version = version.group(1)

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    # Sources are located in the same place as this recipe, copy them to the recipe
    exports_sources = "CMakeLists.txt", "src/*", "include/*"

    def export(self):
        git = Git(self, self.recipe_folder)
        git.coordinates_to_conandata()

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def generate(self):
        tc = CMakeToolchain(self)
        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()

    def layout(self):
        cmake_layout(self)

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["ai"]
