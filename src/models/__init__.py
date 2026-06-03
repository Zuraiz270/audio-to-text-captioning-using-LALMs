from src.models.base import Captioner
from src.models.cnn14_dcase import CNN14DCASECaptioner
from src.models.enclap import EnCLAPCaptioner

MODEL_REGISTRY: dict[str, type[Captioner]] = {
    "cnn14": CNN14DCASECaptioner,
    "enclap": EnCLAPCaptioner,
}
