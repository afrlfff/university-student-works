from dataclasses import dataclass, field
import numpy as np

# @dataclass
# class InputData:
#     V: np.ndarray = field(default_factory=lambda: np.array([]))
#     I: np.ndarray = field(default_factory=lambda: np.array([]))
#     R: float = 1
#     dt: float = 1e-6

#     # additional
#     V_zeros: np.ndarray = field(default_factory=lambda: np.array([]))
#     #
#     incomplete_on_start: bool = False
#     incomplete_on_end: bool = False

#     def is_valid(self) -> bool:
#         return (
#             len(self.V_zeros) > 0
#             and len(self.V) > 0
#             and len(self.I) > 0
#             and len(self.V) == len(self.I)
#             and self.R > 0
#             and self.dt > 0
#         )

@dataclass
class AppState:
    # source data
    V: np.ndarray = field(default_factory=lambda: np.array([]))
    I: np.ndarray = field(default_factory=lambda: np.array([]))
    R: float = 1
    dt: float = 1e-6

    # additional data for source data
    V_zeros: np.ndarray = field(default_factory=lambda: np.array([]))
    V_maxima: np.ndarray = field(default_factory=lambda: np.array([]))
    V_minima: np.ndarray = field(default_factory=lambda: np.array([]))
    incomplete_on_start: bool = False
    incomplete_on_end: bool = False
    first_cycle_idx: int = 0
    last_cycle_idx: int = 0
    starts_with_hrs: bool = False
    g_break_length: int = 0
    V_freq: float = 1.0

    # user configuring params 
    k_set: float = 1.0
    k_reset: float = 1.0

    # shottky
    shottky_params: np.ndarray = field(default_factory=lambda: np.array([]))

    # switching params
    R_on: np.ndarray = field(default_factory=lambda: np.array([]))
    R_off: np.ndarray = field(default_factory=lambda: np.array([]))
    V_set: np.ndarray = field(default_factory=lambda: np.array([]))
    V_reset: np.ndarray = field(default_factory=lambda: np.array([]))

    def is_source_data_valid(self) -> bool:
        return (
            len(self.V) > 0
            and len(self.I) > 0
            and len(self.V) == len(self.I)
            and self.R > 0
            and self.dt > 0
            and len(self.V_zeros) > 0
            and len(self.V_maxima) > 0
            and len(self.V_minima) > 0
            and self.first_cycle_idx >= 0
            and self.last_cycle_idx >= self.first_cycle_idx
        )

    def clear(self) -> None:
        self.V = np.array([])
        self.I = np.array([])
        self.R = 1
        self.dt = 1e-6

        self.V_zeros = np.array([])
        self.V_maxima = np.array([])
        self.V_minima = np.array([])

        self.incomplete_on_start = False
        self.incomplete_on_end = False
        self.first_cycle_idx = 0
        self.last_cycle_idx = 0
        self.starts_with_hrs = False

        self.g_break_length = 3
        self.k_set = 1.0
        self.k_reset = 1.0

        self.shottky_params = np.array([])

        self.R_on = np.array([])
        self.R_off = np.array([])
        self.V_set = np.array([])
        self.V_reset = np.array([])