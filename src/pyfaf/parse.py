# Copyright (C) 2013  ABRT Team
# Copyright (C) 2013  Red Hat, Inc.
#
# This file is part of faf.
#
# faf is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# faf is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with faf.  If not, see <http://www.gnu.org/licenses/>.

__all__ = ["parse_nvra"]


def parse_nvra(pkg):
    """
    Split name-version-release.arch.rpm into
    dictionary.
    """

    result = {}

    if pkg.endswith(".rpm"):
        pkg = pkg[:-4]

    dot = pkg.rfind(".")
    result["arch"] = pkg[dot + 1:]
    pkg = pkg[:dot]

    rel_dash = pkg.rfind("-", 0, dot)
    result["release"] = pkg[rel_dash + 1:dot]

    ver_dash = pkg.rfind("-", 0, rel_dash)
    result["version"] = pkg[ver_dash + 1:rel_dash]
    result["name"] = pkg[:ver_dash]

    return result
