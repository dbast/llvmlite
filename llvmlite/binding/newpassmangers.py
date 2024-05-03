from ctypes import (c_bool, c_int)
from llvmlite.binding import ffi
from llvmlite.binding.initfini import llvm_version_info

llvm_version_major = llvm_version_info[0]


def create_new_module_pass_manager():
    return NewModulePassManager()


def create_new_function_pass_manager():
    return NewFunctionPassManger()


def create_pass_builder(tm, pto):
    return PassBuilder(tm, pto)


def create_pipeline_options():
    return PipelineTuningOptions()


class NewModulePassManager(ffi.ObjectRef):

    def __init__(self, ptr=None):
        if ptr is None:
            ptr = ffi.lib.LLVMPY_CreateNewModulePassManager()
        ffi.ObjectRef.__init__(self, ptr)

    def run(self, module, pb):
        ffi.lib.LLVMPY_NMPRun_module(self, pb, module)

    def addVerifier(self):
        ffi.lib.LLVMPY_AddVeriferPass(self)

    def add_aa_eval_pass(self):
        ffi.lib.LLVMPY_AddAAEvalPass_module(self)

    def add_simplify_cfg_pass(self):
        ffi.lib.LLVMPY_AddSimplifyCFGPass_module(self)

    def add_loop_unroll_pass(self):
        ffi.lib.LLVMPY_AddLoopUnrollPass_module(self)

    def add_loop_rotate_pass(self):
        ffi.lib.LLVMPY_LLVMAddLoopRotatePass_module(self)

    def add_instruction_combine_pass(self):
        ffi.lib.LLVMPY_LLVMAddInstructionCombinePass_module(self)

    def add_jump_threading_pass(self, threshold=-1):
        ffi.lib.LLVMPY_AddJumpThreadingPass_module(self, threshold)

    # What will happen to the pointer to objects created with run() method
    def _dispose(self):
        ffi.lib.LLVMPY_DisposeNewModulePassManger(self)


class NewFunctionPassManger(ffi.ObjectRef):

    def __init__(self, ptr=None):
        if ptr is None:
            ptr = ffi.lib.LLVMPY_CreateNewFunctionPassManager()
        ffi.ObjectRef.__init__(self, ptr)

    def add_aa_eval_pass(self):
        ffi.lib.LLVMPY_AddAAEvalPass_function(self)

    def add_simplify_cfg_pass(self):
        ffi.lib.LLVMPY_AddSimplifyCFGPass_function(self)

    def run(self, fun, pb):
        ffi.lib.LLVMPY_NMPRun_function(self, pb, fun)

    def add_loop_unroll_pass(self):
        ffi.lib.LLVMPY_AddLoopUnrollPass_function(self)

    def add_loop_rotate_pass(self):
        ffi.lib.LLVMPY_LLVMAddLoopRotatePass_function(self)

    def add_instruction_combine_pass(self):
        ffi.lib.LLVMPY_LLVMAddInstructionCombinePass_function(self)

    def add_jump_threading_pass(self, threshold=-1):
        ffi.lib.LLVMPY_AddJumpThreadingPass_function(self, threshold)

    def _dispose(self):
        ffi.lib.LLVMPY_DisposeNewFunctionPassManger(self)


# Make this nested class of PassBuilder?
class PipelineTuningOptions(ffi.ObjectRef):

    def __init__(self, ptr=None):
        if ptr is None:
            ptr = ffi.lib.LLVMPY_CreatePipelineTuningOptions()
            self._opt_level = 3
            # self._size_level = 0
        ffi.ObjectRef.__init__(self, ptr)

    @property
    def loop_interleaving(self):
        return ffi.lib.LLVMPY_PTOGetLoopInterleaving(self)

    @loop_interleaving.setter
    def loop_interleaving(self, value):
        ffi.lib.LLVMPY_PTOSetLoopInterleaving(self, value)

    @property
    def loop_vectorization(self):
        return ffi.lib.LLVMPY_PTOGetLoopVectorization(self)

    @loop_vectorization.setter
    def loop_vectorization(self, value):
        ffi.lib.LLVMPY_PTOSetLoopVectorization(self, value)

    @property
    def slp_vectorization(self):
        return ffi.lib.LLVMPY_PTOGetSLPVectorization(self)

    @slp_vectorization.setter
    def slp_vectorization(self, value):
        ffi.lib.LLVMPY_PTOSetSLPVectorization(self, value)

    @property
    def loop_unrolling(self):
        return ffi.lib.LLVMPY_PTOGetLoopUnrolling(self)

    @loop_unrolling.setter
    def loop_unrolling(self, value):
        ffi.lib.LLVMPY_PTOSetLoopUnrolling(self, value)

    # // FIXME: Available from llvm16
    # @property
    # def inlining_threshold(self):
    #     return ffi.lib.LLVMPY_PTOGetInlinerThreshold(self)

    # @inlining_threshold.setter
    # def inlining_threshold(self, value):
    #     ffi.lib.LLVMPY_PTOSetInlinerThreshold(self, value)

    # Not part of PTO
    @property
    def opt_level(self):
        """
        The general optimization level as an integer between 0 and 3.
        """
        return self._opt_level

    @opt_level.setter
    def opt_level(self, level):
        self._opt_level = level

    # FIXME: Model optimization level combining opt level and
    # size level similar to llvm
    # @property
    # def size_level(self):
    #     """
    #     Whether and how much to optimize for size.
    #     An integer between 0 and 2.
    #     """
    #     return self._size_level

    # @size_level.setter
    # def size_level(self, size):
    #     self._size_level = size

    def _dispose(self):
        ffi.lib.LLVMPY_DisposePipelineTuningOptions(self)


class PassBuilder(ffi.ObjectRef):

    def __init__(self, tm, pto, ptr=None):
        if ptr is None:
            self._pto = pto
            self._tm = tm
            ptr = ffi.lib.LLVMPY_CreatePassBuilder(tm, pto)
        ffi.ObjectRef.__init__(self, ptr)

    def getNewModulePassManager(self):
        return NewModulePassManager(
            ffi.lib.LLVMPY_buildPerModuleDefaultPipeline(
                self, self._pto.opt_level)
        )

    def getNewFunctionPassManager(self):
        return NewFunctionPassManger(
            ffi.lib.LLVMPY_buildFunctionSimplificationPipeline(
                self, self._pto.opt_level)
        )

    def _dispose(self):
        # Should I explicitly delete pointer to pto and tm?
        ffi.lib.LLVMPY_DisposePassBuilder(self)


# ============================================================================
# FFI


ffi.lib.LLVMPY_CreateNewModulePassManager.restype = ffi.LLVMModulePassManagerRef

ffi.lib.LLVMPY_NMPRun_module.argtypes = [ffi.LLVMModulePassManagerRef,
                                         ffi.LLVMPassBuilderRef,
                                         ffi.LLVMModuleRef,]

ffi.lib.LLVMPY_AddVeriferPass.argtypes = [ffi.LLVMModulePassManagerRef,]
ffi.lib.LLVMPY_AddAAEvalPass_module.argtypes = [ffi.LLVMModulePassManagerRef,]
ffi.lib.LLVMPY_AddSimplifyCFGPass_module.argtypes = [
    ffi.LLVMModulePassManagerRef,]

ffi.lib.LLVMPY_AddLoopUnrollPass_module.argtypes = [
    ffi.LLVMModulePassManagerRef,]

ffi.lib.LLVMPY_LLVMAddLoopRotatePass_module.argtypes = [
    ffi.LLVMModulePassManagerRef,]

ffi.lib.LLVMPY_LLVMAddInstructionCombinePass_module.argtypes = [
    ffi.LLVMModulePassManagerRef,]

ffi.lib.LLVMPY_AddJumpThreadingPass_module.argtypes = [
    ffi.LLVMModulePassManagerRef,]

ffi.lib.LLVMPY_DisposeNewModulePassManger.argtypes = [
    ffi.LLVMModulePassManagerRef,]

ffi.lib.LLVMPY_CreateNewFunctionPassManager.restype = \
    ffi.LLVMFunctionPassManagerRef

ffi.lib.LLVMPY_NMPRun_function.argtypes = [ffi.LLVMFunctionPassManagerRef,
                                           ffi.LLVMPassBuilderRef,
                                           ffi.LLVMValueRef,]

ffi.lib.LLVMPY_AddAAEvalPass_function.argtypes = [
    ffi.LLVMFunctionPassManagerRef,]

ffi.lib.LLVMPY_AddSimplifyCFGPass_function.argtypes = [
    ffi.LLVMFunctionPassManagerRef,]

ffi.lib.LLVMPY_AddLoopUnrollPass_function.argtypes = [
    ffi.LLVMFunctionPassManagerRef,]

ffi.lib.LLVMPY_LLVMAddLoopRotatePass_function.argtypes = [
    ffi.LLVMFunctionPassManagerRef,]

ffi.lib.LLVMPY_LLVMAddInstructionCombinePass_function.argtypes = [
    ffi.LLVMFunctionPassManagerRef,]

ffi.lib.LLVMPY_AddJumpThreadingPass_function.argtypes = [
    ffi.LLVMFunctionPassManagerRef, c_int,]

ffi.lib.LLVMPY_DisposeNewFunctionPassManger.argtypes = [
    ffi.LLVMFunctionPassManagerRef,]

ffi.lib.LLVMPY_CreatePassBuilder.restype = ffi.LLVMPassBuilderRef
ffi.lib.LLVMPY_CreatePassBuilder.argtypes = [ffi.LLVMTargetMachineRef,
                                             ffi.LLVMPipelineTuningOptionsRef,]

ffi.lib.LLVMPY_buildPerModuleDefaultPipeline.restype = \
    ffi.LLVMModulePassManagerRef

ffi.lib.LLVMPY_buildPerModuleDefaultPipeline.argtypes = [
    ffi.LLVMPassBuilderRef, c_int,]

ffi.lib.LLVMPY_buildFunctionSimplificationPipeline.restype = \
    ffi.LLVMFunctionPassManagerRef

ffi.lib.LLVMPY_buildFunctionSimplificationPipeline.argtypes = [
    ffi.LLVMPassBuilderRef, c_int,]

ffi.lib.LLVMPY_DisposePassBuilder.argtypes = [ffi.LLVMPassBuilderRef,]

ffi.lib.LLVMPY_CreatePipelineTuningOptions.restype = \
    ffi.LLVMPipelineTuningOptionsRef

ffi.lib.LLVMPY_PTOGetLoopInterleaving.restype = c_bool
ffi.lib.LLVMPY_PTOGetLoopInterleaving.argtypes = [
    ffi.LLVMPipelineTuningOptionsRef,]

ffi.lib.LLVMPY_PTOSetLoopInterleaving.argtypes = [
    ffi.LLVMPipelineTuningOptionsRef, c_bool]

ffi.lib.LLVMPY_PTOGetLoopVectorization.restype = c_bool
ffi.lib.LLVMPY_PTOGetLoopVectorization.argtypes = [
    ffi.LLVMPipelineTuningOptionsRef,]

ffi.lib.LLVMPY_PTOSetLoopVectorization.argtypes = [
    ffi.LLVMPipelineTuningOptionsRef, c_bool]

ffi.lib.LLVMPY_PTOGetSLPVectorization.restype = c_bool
ffi.lib.LLVMPY_PTOGetSLPVectorization.argtypes = [
    ffi.LLVMPipelineTuningOptionsRef,]

ffi.lib.LLVMPY_PTOSetSLPVectorization.argtypes = [
    ffi.LLVMPipelineTuningOptionsRef, c_bool]

ffi.lib.LLVMPY_PTOGetLoopUnrolling.restype = c_bool
ffi.lib.LLVMPY_PTOGetLoopUnrolling.argtypes = [
    ffi.LLVMPipelineTuningOptionsRef,]

ffi.lib.LLVMPY_PTOSetLoopUnrolling.argtypes = [
    ffi.LLVMPipelineTuningOptionsRef, c_bool]

ffi.lib.LLVMPY_DisposePipelineTuningOptions.argtypes = \
    [ffi.LLVMPipelineTuningOptionsRef,]
