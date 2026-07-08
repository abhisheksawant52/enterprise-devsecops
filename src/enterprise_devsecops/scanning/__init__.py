"""Scanner implementations used by the scanning orchestration layer."""

from enterprise_devsecops.scanning.base import Scanner
from enterprise_devsecops.scanning.container import ContainerScanner
from enterprise_devsecops.scanning.sast import SastScanner
from enterprise_devsecops.scanning.sca import ScaScanner

__all__ = ["Scanner", "SastScanner", "ScaScanner", "ContainerScanner"]

SCANNER_REGISTRY: dict[str, type[Scanner]] = {
    "sast": SastScanner,
    "sca": ScaScanner,
    "container": ContainerScanner,
}
