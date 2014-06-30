#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_assemble
----------------------------------

Tests for `assemble` module.
"""
import pytest
from assemble import assemble


def test_sh_for_success_msg():
    assert assemble.sh("ls -la") == None


def test_sh_for_success_msg():
    with pytest.raises(SystemExit) as exc:
        assert assemble.sh("cp foo.py foo1.py")
