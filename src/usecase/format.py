# データ整形に関するユースケース

from dataclasses import dataclass
from typing import Protocol

import model


#データ整形
@dataclass
class FormatDataInput:
	url:model.URL

@dataclass
class FormatDataOutput:
	data:model.Data


class DataFormatter(Protocol):
    def FormatData(self, input: FormatDataInput) -> FormatDataOutput:
        ...
        