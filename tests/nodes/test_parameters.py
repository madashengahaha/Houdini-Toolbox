"""Test the ht.nodes.parameters module."""

# =============================================================================
# IMPORTS
# =============================================================================

# Standard Library Imports
import os

# Third Party Imports
import pytest

# Houdini Toolbox Imports
import ht.nodes.parameters

# Houdini Imports
import hou


# =============================================================================
# FIXTURES
# =============================================================================


@pytest.fixture(scope="module")
def load_test_file():
    """Load the test hip file."""
    hou.hipFile.load(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "data",
            "test_parameters.hipnc",
        ),
        ignore_load_warnings=True,
    )

    yield

    hou.hipFile.clear()


# Need to ensure the hip file gets loaded.
pytestmark = pytest.mark.usefixtures("load_test_file")


# =============================================================================
# TESTS
# =============================================================================


def test_find_parameters_using_variable():
    """Test ht.nodes.parameters.find_parameters_using_variable."""
    result = ht.nodes.parameters.find_parameters_using_variable("BAR")

    assert result == ()

    expected = (
        hou.parm("/obj/geo1/font1/text"),
        hou.parm("/out/mantra1/vm_picture"),
        hou.parm("/out/mantra1/soho_diskfile"),
        hou.parm("/out/mantra1/vm_dcmfilename"),
        hou.parm("/out/mantra1/vm_dsmfilename"),
        hou.parm("/out/mantra1/vm_tmpsharedstorage"),
        hou.parm("/tasks/topnet1/taskgraphfile"),
        hou.parm("/tasks/topnet1/localscheduler/pdg_workingdir"),
    )

    result = ht.nodes.parameters.find_parameters_using_variable("HIP")

    assert result == expected

    expected = (
        hou.parm("/out/mantra1/vm_picture"),
        hou.parm("/tasks/topnet1/taskgraphfile"),
        hou.parm("/tasks/topnet1/localscheduler/tempdircustom"),
    )

    result = ht.nodes.parameters.find_parameters_using_variable("$HIPNAME")

    assert result == expected

    expected = (hou.parm("/obj/geo1/font2/text"),)

    result = ht.nodes.parameters.find_parameters_using_variable("$HIPFILE")

    assert result == expected

    expected = (
        hou.parm("/obj/geo1/font1/text"),
        hou.parm("/tasks/topnet1/taskgraphfile"),
    )

    result = ht.nodes.parameters.find_parameters_using_variable("F")

    assert result == expected

    expected = (hou.parm("/out/mantra1/vm_picture"),)

    result = ht.nodes.parameters.find_parameters_using_variable("$F4")

    assert result == expected


def test_find_parameters_with_value():
    """Test ht.nodes.parameters.find_parameters_with_value."""
    result = ht.nodes.parameters.find_parameters_with_value("gaussian")
    assert result == (hou.parm("/out/mantra1/vm_pfilter"),)

    result = ht.nodes.parameters.find_parameters_with_value("render1")
    assert result == ()

    result = ht.nodes.parameters.find_parameters_with_value("render")
    assert result == (
        hou.parm("/obj/geo1/font1/text"),
        hou.parm("/out/mantra1/vm_picture"),
    )

    result = ht.nodes.parameters.find_parameters_with_value("renders")
    assert result == (hou.parm("/obj/geo1/font2/text"),)
