
class Generator:
  def __init__(self, prefix: str):
    self.prefix = prefix
    self.current = 0

  def get_next(self) -> str:
    self.current += 1
    return f"{self.prefix}{self.current}"

class LabelGenerator(Generator):

  def __init__(self):
    super().__init__("L")
