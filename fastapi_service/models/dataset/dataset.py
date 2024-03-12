from pydantic import BaseModel

# equivalent of
# enum DatasetType {
#     OED = 0;
#     UD_FILTERED = 1;
#     UD_UNFILTERED = 2;
# }

class DatasetType(BaseModel):
    name: str = "OED" # "OED" | "UD_FILTERED" | "UD_UNFILTERED
