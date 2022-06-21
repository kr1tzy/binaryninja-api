
import ctypes
import inspect
from typing import Generator, Optional, List, Tuple, Union, Mapping, Any, Dict
from dataclasses import dataclass

from binaryninja import DataVariable

from . import function
from . import _binaryninjacore as core
from binaryninja.types import Type

from . import binaryview


class Component:
    def __init__(self, view=None, handle=None):

        self.view: binaryview.BinaryView = view

        if not handle:
            self.handle = core.BNComponentCreateEmpty()
        else:
            self.handle = handle

        self.guid = core.BNComponentGetGUID(self.handle)

    def __repr__(self):
        return f'<Component "{self.guid[:8]}...">'

    def add_function(self, func: function.Function) -> None:
        core.BNComponentAddFunctionReference(self.handle, func.handle, True)

    def contains_function(self, func: function.Function) -> bool:
        return core.BNComponentContainsFunction(self.handle, func.handle)

    def remove_function(self, func: function.Function) -> None:
        core.BNComponentRemoveFunctionReference(self.handle, func.handle, True)

    def add_component(self, component: 'Component') -> None:
        core.BNComponentAddComponentReference(self.handle, component.handle)

    def contains_component(self, component: 'Component') -> bool:
        return core.BNComponentContainsComponent(self.handle, component.handle)

    def remove_component(self, component: 'Component') -> None:
        core.BNComponentRemoveComponentReference(self.handle, component.handle)

    @property
    def name(self):
        return core.BNComponentGetName(self.handle)

    @name.setter
    def name(self, _name):
        core.BNComponentSetName(self.handle, _name)

    @property
    def components(self) -> List['Component']:
        components = []
        count = ctypes.c_ulonglong(0)
        bn_components = core.BNComponentGetContainedComponents(self.handle, count)

        for i in range(count.value):
            bn_component = core.BNNewComponentReference(bn_components[i])
            component = Component(self.view, bn_component)
            components.append(component)

        core.BNComponentFreeContainedComponentList(bn_components, count.value)
        return components

    @property
    def functions(self) -> List[function.Function]:
        functions = []
        count = ctypes.c_ulonglong(0)
        bn_functions = core.BNComponentGetContainedFunctions(self.handle, count)

        for i in range(count.value):
            bn_component = bn_functions[i]
            component = function.Function(self.view, bn_component)
            functions.append(component)

        core.BNComponentFreeContainedFunctionList(bn_functions, count.value)
        return functions

    def get_referenced_data_variables(self, recursive=False):
        data_vars = []
        count = ctypes.c_ulonglong(0)
        if recursive:
            bn_data_vars = core.BNComponentGetReferencedDataVariablesRecursive(self.handle, count)
        else:
            bn_data_vars = core.BNComponentGetReferencedDataVariables(self.handle, count)

        for i in range(count.value):
            bn_data_var = bn_data_vars[i]
            data_var = DataVariable.from_core_struct(bn_data_var, self.view)
            data_vars.append(data_var)

        core.BNComponentFreeReferencedDataVariableList(bn_data_vars, count.value)
        return data_vars

    def get_referenced_types(self, recursive=False):
        types = []
        count = ctypes.c_ulonglong(0)

        bn_types = core.BNComponentGetReferencedTypes(self.handle, count)

        for i in range(count.value):
            bn_type = core.BNNewTypeReference(bn_types[i])
            _type = Type(bn_type)
            types.append(_type)

        core.BNComponentFreeReferencedTypesList(bn_types, count.value)

        return types
