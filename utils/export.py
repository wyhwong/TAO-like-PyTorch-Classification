import torch
import onnx

from .common import getLogger

LOGGER = getLogger("Export")
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

def exportModelToONNX(model, height:int, width:int, exportPath:str) -> None:
    LOGGER.debug(f"Changing model to evaluation mode.")
    model.eval()
    LOGGER.debug(f"Generating a random input for exporting.")
    x = torch.randn(1, 3, height, width, requires_grad=True)
    LOGGER.debug(f"Exporting the model: {exportPath=}.")
    torch.onnx.export(model,
                      x.to(DEVICE),
                      exportPath,
                      export_params=True,
                      opset_version=10,
                      do_constant_folding=True,
                      input_names = ['input'],
                      output_names = ['output'])
    LOGGER.info(f"Successfully exported the model: {exportPath=}.")


def checkModelIsValid(modelPath:str) -> None:
    LOGGER.info(f"Checking onnx model at {modelPath}")
    onnx_model = onnx.load(modelPath)
    onnx.checker.check_model(onnx_model)
    LOGGER.info(f"Checked onnx model at {modelPath}")
