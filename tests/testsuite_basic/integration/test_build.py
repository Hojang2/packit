# MIT License
#
# Copyright (c) 2018-2019 Red Hat, Inc.

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
from flexmock import flexmock

from packit.api import PackitAPI
from packit.config import get_local_package_config
from packit.local_project import LocalProject
from tests.testsuite_basic.spellbook import get_test_config
from packit.utils import cwd

from packit import utils


def test_basic_build(upstream_n_distgit, mock_remote_functionality_upstream):
    u, d = upstream_n_distgit

    with cwd(u):
        c = get_test_config()

        pc = get_local_package_config(str(u))
        pc.upstream_project_url = str(u)
        pc.dist_git_clone_path = str(d)
        up_lp = LocalProject(working_dir=u)

        api = PackitAPI(c, pc, up_lp)
        flexmock(utils).should_receive("run_command").with_args(
            cmd=["fedpkg", "build", "--scratch", "--nowait", "--target", "asdqwe"],
            cwd=api.dg.local_project.working_dir,
            error_message="Submission of build to koji failed.",
            fail=True,
        ).once()
        api.build("master", scratch=True, nowait=True, koji_target="asdqwe")
