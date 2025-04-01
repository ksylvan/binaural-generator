"""Functions for generating different types of background noise."""

import numpy as np
from scipy.fft import fft, ifft


def generate_white_noise(num_samples: int) -> np.ndarray:
    """Generates white noise.

    Args:
        num_samples: The number of samples to generate.

    Returns:
        A numpy array containing white noise samples.
    """
    if num_samples <= 0:
        return np.array([])
    # Generate random samples from a standard normal distribution
    noise = np.random.randn(num_samples)
    # Normalize to range [-1, 1] assuming practical limits
    noise /= np.max(np.abs(noise)) if np.max(np.abs(noise)) > 0 else 1
    return noise


def generate_pink_noise(num_samples: int) -> np.ndarray:
    """Generates pink noise using the FFT filtering method.

    Pink noise has a power spectral density proportional to 1/f.

    Args:
        num_samples: The number of samples to generate.

    Returns:
        A numpy array containing pink noise samples.
    """
    if num_samples <= 0:
        return np.array([])

    # Generate white noise
    white_noise = np.random.randn(num_samples)

    # Compute FFT
    fft_white = fft(white_noise)

    # Create frequency scaling factor (1/sqrt(f))
    frequencies = np.fft.fftfreq(num_samples)
    # Avoid division by zero for the DC component (f=0)
    # Set DC component scaling to 1 (or 0, results differ slightly, 1 is common)
    scaling = np.ones_like(frequencies)
    non_zero_freq_indices = frequencies != 0
    scaling[non_zero_freq_indices] = 1.0 / np.sqrt(
        np.abs(frequencies[non_zero_freq_indices])
    )

    # Apply scaling to FFT
    fft_pink = fft_white * scaling

    # Compute inverse FFT
    pink_noise = np.real(ifft(fft_pink))

    # Normalize to range [-1, 1]
    pink_noise /= np.max(np.abs(pink_noise)) if np.max(np.abs(pink_noise)) > 0 else 1
    return pink_noise


def generate_brown_noise(num_samples: int) -> np.ndarray:
    """Generates brown noise (Brownian noise or 1/f^2 noise).

    Brown noise is generated by integrating white noise (random walk).

    Args:
        num_samples: The number of samples to generate.

    Returns:
        A numpy array containing brown noise samples.
    """
    if num_samples <= 0:
        return np.array([])

    # Generate white noise (steps of the random walk)
    white_noise = np.random.randn(num_samples)

    # Integrate white noise using cumulative sum
    brown_noise = np.cumsum(white_noise)

    # Normalize to range [-1, 1]
    brown_noise -= np.mean(brown_noise)  # Center around zero
    brown_noise /= np.max(np.abs(brown_noise)) if np.max(np.abs(brown_noise)) > 0 else 1
    return brown_noise
