"""合成 pathly 五支 UI 音效 → frontend/public/sounds/*.wav。

設計規則（對應 TONE_CHARTER：自然聲、無旋律、極低音量）：
- 全部單聲道 44.1kHz、16-bit
- 源振幅壓在 0.55 以下；SoundProvider 還會再衰減 10–20% 播放
- 無旋律：bell / chime 只有「單次敲擊 + 自然泛音」，不構成音階
- 無通知感：避免 DX7 類合成音色，所有聲音都加短暫呼吸/噪音紋理

重跑：  python scripts/make_sounds.py
"""

from __future__ import annotations

import math
import random
import struct
import wave
from pathlib import Path

SAMPLE_RATE = 44_100
OUT_DIR = Path(__file__).resolve().parent.parent / "frontend" / "public" / "sounds"


# --- helpers ---------------------------------------------------------------

def normalize(samples: list[float], target_peak: float = 0.8) -> list[float]:
    """正規化到統一峰值，讓 SoundProvider 的音量表成為唯一可調參數。"""
    peak = max(abs(s) for s in samples) or 1e-9
    gain = target_peak / peak
    return [s * gain for s in samples]


def write_wav(samples: list[float], path: Path) -> None:
    samples = normalize(samples, target_peak=0.8)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SAMPLE_RATE)
        buf = b"".join(
            struct.pack("<h", int(max(-1.0, min(1.0, s)) * 32767)) for s in samples
        )
        w.writeframes(buf)


def exp_decay(n: int, tau_ms: float) -> list[float]:
    tau = SAMPLE_RATE * tau_ms / 1000
    return [math.exp(-i / tau) for i in range(n)]


def soft_attack(samples: list[float], attack_ms: float) -> None:
    """in-place fade-in 避免 click"""
    a = int(SAMPLE_RATE * attack_ms / 1000)
    for i in range(min(a, len(samples))):
        samples[i] *= i / a


def soft_release(samples: list[float], release_ms: float) -> None:
    """in-place fade-out 避免尾部斷切"""
    r = int(SAMPLE_RATE * release_ms / 1000)
    n = len(samples)
    for i in range(min(r, n)):
        samples[n - 1 - i] *= i / r


def lowpass(samples: list[float], cutoff_hz: float, passes: int = 1) -> list[float]:
    dt = 1 / SAMPLE_RATE
    rc = 1 / (2 * math.pi * cutoff_hz)
    alpha = dt / (rc + dt)
    out = list(samples)
    for _ in range(passes):
        prev = 0.0
        for i, x in enumerate(out):
            prev = prev + alpha * (x - prev)
            out[i] = prev
    return out


# --- sounds ----------------------------------------------------------------

def make_air() -> list[float]:
    """200ms 空氣聲：低頻白噪 + 柔緩 envelope，像吹進紙上的一口氣。"""
    n = int(SAMPLE_RATE * 0.22)
    random.seed(1)
    noise = [random.uniform(-1, 1) for _ in range(n)]
    noise = lowpass(noise, 2200, passes=2)
    out = list(noise)
    soft_attack(out, 30)
    # 衰減尾
    tail = exp_decay(n, 120)
    out = [out[i] * tail[i] * 0.35 for i in range(n)]
    soft_release(out, 30)
    return out


def make_wood() -> list[float]:
    """300ms 木聲：短噪音 transient + 低頻阻尼震盪（280Hz），像指節敲木桌。"""
    n = int(SAMPLE_RATE * 0.32)
    random.seed(2)
    # 敲擊 transient
    noise = [random.uniform(-1, 1) for _ in range(n)]
    noise = lowpass(noise, 3000)
    ntail = exp_decay(n, 25)
    transient = [noise[i] * ntail[i] * 0.55 for i in range(n)]
    # 木頭本體：280Hz 主音 + 520Hz 泛音，快速阻尼
    body_decay = exp_decay(n, 55)
    body = [
        (
            0.35 * math.sin(2 * math.pi * 280 * i / SAMPLE_RATE)
            + 0.12 * math.sin(2 * math.pi * 520 * i / SAMPLE_RATE)
        ) * body_decay[i]
        for i in range(n)
    ]
    out = [transient[i] + body[i] for i in range(n)]
    soft_release(out, 20)
    return out


def make_bell() -> list[float]:
    """800ms 低鈴聲：單次敲響的鐘體，三個自然泛音（1 : 1.5 : 2），長衰減。
    非旋律——只是同時響起的單一和聲事件。"""
    n = int(SAMPLE_RATE * 0.85)
    decay = exp_decay(n, 240)
    f1, f2, f3 = 440, 660, 880
    out = [
        (
            0.50 * math.sin(2 * math.pi * f1 * i / SAMPLE_RATE)
            + 0.28 * math.sin(2 * math.pi * f2 * i / SAMPLE_RATE)
            + 0.14 * math.sin(2 * math.pi * f3 * i / SAMPLE_RATE)
        ) * decay[i] * 0.50
        for i in range(n)
    ]
    soft_attack(out, 8)
    soft_release(out, 40)
    return out


def make_drop() -> list[float]:
    """400ms 水滴聲：頻率在 30ms 內從 700→1300Hz 快速上翹，再向 450Hz 下墜。"""
    n = int(SAMPLE_RATE * 0.42)
    decay = exp_decay(n, 90)
    phase = 0.0
    out = []
    for i in range(n):
        t = i / SAMPLE_RATE
        if t < 0.03:
            f = 700 + (1300 - 700) * (t / 0.03)
        else:
            f = 1300 - (1300 - 450) * min(1, (t - 0.03) / 0.26)
        phase += 2 * math.pi * f / SAMPLE_RATE
        out.append(math.sin(phase) * decay[i] * 0.45)
    # 前端 plip 噪音顆粒
    random.seed(3)
    noise = [random.uniform(-1, 1) for _ in range(n)]
    noise = lowpass(noise, 4000)
    plip = exp_decay(n, 12)
    for i in range(n):
        out[i] += noise[i] * plip[i] * 0.18
    soft_release(out, 30)
    return out


def make_chime() -> list[float]:
    """1.2s 柔和共鳴：三泛音同時響起（G4 + 五度 + 八度），慢 attack、超長尾。
    前段混入低頻呼吸噪音 0.08 的極淡層，讓起音不像合成器。"""
    n = int(SAMPLE_RATE * 1.25)
    decay = exp_decay(n, 380)
    f1, f2, f3 = 392, 588, 784  # G4, 五度, 八度
    out = [
        (
            0.50 * math.sin(2 * math.pi * f1 * i / SAMPLE_RATE)
            + 0.28 * math.sin(2 * math.pi * f2 * i / SAMPLE_RATE)
            + 0.16 * math.sin(2 * math.pi * f3 * i / SAMPLE_RATE)
        ) * decay[i] * 0.45
        for i in range(n)
    ]
    soft_attack(out, 60)  # 慢起，呼吸感
    # 起音端的呼吸雜訊層
    random.seed(4)
    noise = [random.uniform(-1, 1) for _ in range(n)]
    noise = lowpass(noise, 1400, passes=2)
    breath_len = int(SAMPLE_RATE * 0.25)
    breath = exp_decay(breath_len, 90)
    for i in range(breath_len):
        out[i] += noise[i] * breath[i] * 0.07
    soft_release(out, 120)
    return out


# --- main ------------------------------------------------------------------

def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    builders = {
        "air": make_air,
        "wood": make_wood,
        "bell": make_bell,
        "drop": make_drop,
        "chime": make_chime,
    }
    for name, builder in builders.items():
        path = OUT_DIR / f"{name}.wav"
        write_wav(builder(), path)
        print(f"wrote {path.name}  ({path.stat().st_size / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
