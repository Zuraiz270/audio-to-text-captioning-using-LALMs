from src.models.base import Captioner
from src.models.ast_tagging import ASTTaggingCaptioner
from src.models.cnn14_dcase import CNN14DCASECaptioner
from src.models.enclap import EnCLAPCaptioner
from src.models.qwen_omni import QwenOmniCaptioner
from src.models.salmonn import SalmonnCaptioner

MODEL_REGISTRY: dict[str, type[Captioner]] = {
    "cnn14": CNN14DCASECaptioner,
    "enclap": EnCLAPCaptioner,
    "ast": ASTTaggingCaptioner,
    "qwen_omni": QwenOmniCaptioner,
    "salmonn": SalmonnCaptioner,
}
