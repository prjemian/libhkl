"""Test that libhkl pre-built support is available in Python."""

import gi  # gobject-introspection, to access libhkl

gi.require_version("Hkl", "5.0")
from gi.repository import Hkl as libhkl  # noqa: E402

# access some content
assert "VERSION" in dir(libhkl)
print(f"{libhkl.VERSION=}")

diffractometer_types = libhkl.factories()
assert isinstance(diffractometer_types, dict)
assert 5 < len(diffractometer_types) < 50
for i, dt in enumerate(sorted(diffractometer_types), start=1):
    print(f"{i}\t{dt}")

UserUnits = libhkl.UnitEnum.USER
assert UserUnits is not None

DefaultUnits = libhkl.UnitEnum.DEFAULT
assert DefaultUnits is not None

# ------ E4CV

TEST_GEOMETRY = "E4CV"
print(f"Testing geometry {TEST_GEOMETRY}")
TEST_AXIS_LIST = "omega chi phi tth".split()
TEST_ENGINE = "hkl"
TEST_MODES = """
bissector
constant_omega
constant_chi
constant_phi
double_diffraction
psi_constant
""".strip().splitlines()

factory = diffractometer_types[TEST_GEOMETRY]
engine_list = factory.create_new_engine_list()
engine_names = [e.name_get() for e in engine_list.engines_get()]
assert TEST_ENGINE in engine_names

engine = engine_list.engine_get_by_name(TEST_ENGINE)
assert engine.modes_names_get() == TEST_MODES, f"{engine.modes_names_get()=}"

geometry = factory.create_new_geometry()
assert geometry.axis_names_get() == TEST_AXIS_LIST

# -------- APS POLAR

TEST_GEOMETRY = "APS POLAR"
print(f"Testing geometry {TEST_GEOMETRY}")
TEST_AXIS_LIST = "tau mu chi phi gamma delta".split()
TEST_ENGINE = "hkl"
TEST_MODES = """
4-circles constant phi horizontal
zaxis + alpha-fixed
zaxis + beta-fixed
zaxis + alpha=beta
4-circles bissecting horizontal
4-circles constant omega horizontal
4-circles constant chi horizontal
lifting detector mu
lifting detector omega
lifting detector chi
lifting detector phi
psi constant horizontal
""".strip().splitlines()

factory = diffractometer_types[TEST_GEOMETRY]
engine_list = factory.create_new_engine_list()
engine_names = [e.name_get() for e in engine_list.engines_get()]
assert TEST_ENGINE in engine_names
engine = engine_list.engine_get_by_name(TEST_ENGINE)
assert engine.modes_names_get() == TEST_MODES, f"{engine.modes_names_get()=}"

geometry = factory.create_new_geometry()
assert geometry.axis_names_get() == TEST_AXIS_LIST

print("All tests finished successfully.")
