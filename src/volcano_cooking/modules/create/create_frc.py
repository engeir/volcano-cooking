"""Create volcanic forcing as a Poisson process with power law amplitudes."""

from abc import ABC, abstractmethod
from typing import Callable, Tuple

import numpy as np
import scipy.stats as scp_stats
from fppy import model


class PoissonDistForcingGenerator(model.ForcingGenerator):
    """Generates a forcing with Poisson distributed number of pulses.

    Generates a standard forcing, but with Poisson distributed number of pulses and
    uniformly distributed arrival times. The resulting process is therefore a Poisson
    process. Amplitude and duration distributions can be customized.
    """

    def __init__(self):
        self._amplitude_distribution = None
        self._duration_distribution = None

    def get_forcing(self, times: np.ndarray, gamma: float) -> model.Forcing:
        total_pulses = int(max(times) * gamma)
        total_pulses = np.random.poisson(lam=total_pulses)
        arrival_times = np.random.default_rng().uniform(
            low=times[0], high=times[len(times) - 1], size=total_pulses
        )
        amplitudes = self._get_amplitudes(total_pulses)
        durations = self._get_durations(total_pulses)
        return model.Forcing(total_pulses, arrival_times, amplitudes, durations)

    def set_amplitude_distribution(
        self,
        amplitude_distribution_function: Callable[[int], np.ndarray],
    ):
        self._amplitude_distribution = amplitude_distribution_function

    def set_duration_distribution(
        self, duration_distribution_function: Callable[[int], np.ndarray]
    ):
        self._duration_distribution = duration_distribution_function

    def _get_amplitudes(self, total_pulses) -> np.ndarray:
        if self._amplitude_distribution is not None:
            return self._amplitude_distribution(total_pulses)
        return np.random.default_rng().exponential(scale=1.0, size=total_pulses)

    def _get_durations(self, total_pulses) -> np.ndarray:
        if self._duration_distribution is not None:
            return self._duration_distribution(total_pulses)
        return np.ones(total_pulses)


class SynthFrc(ABC):
    @abstractmethod
    def get_frc(self) -> Tuple[np.ndarray, np.ndarray]:
        """Return time and a realisation of the synthetic forcing signal."""


class Frf(SynthFrc):
    def __init__(self, fs: float = 1) -> None:
        # Lomax
        self.fs = fs
        self.fpp = model.FPPModel(gamma=0.1, total_duration=9999, dt=1 / self.fs)
        # self.fpp.set_pulse_shape(pulse_shape.StandardPulseGenerator("2-exp", lam=0.35))
        my_forcing_gen = PoissonDistForcingGenerator()
        # my_forcing_gen = model.StandardForcingGenerator()
        my_forcing_gen.set_amplitude_distribution(lambda k: self.__lomax_amp(k, 1.8))
        self.fpp.set_custom_forcing_generator(my_forcing_gen)
        # my_pulseshape_gen = DoubleExponentialShortPulseGenerator(0.2, 0.2, 0.1, 0.8)
        # self.fpp.set_pulse_shape(my_pulseshape_gen)

    def __lomax_amp(self, k: int, c: float) -> np.ndarray:
        r = scp_stats.lomax.rvs(c, size=k)
        return r

    def get_frc(self) -> Tuple[np.ndarray, np.ndarray]:
        t, f = self.fpp.make_realization()
        # Roll the highest peak to the middle
        # shift = int(len(f) / 2) - np.argmax(f)
        # f = np.roll(f, shift)
        return t, f
