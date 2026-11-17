from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

ALPHA = 80.0
LAMBDA = 1 / 40
A = 10.0
SAMPLE_SIZES = (100, 1000, 10000)
SEED = 42

SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR / "output/"


class Distribution:
    UNIFORM = 0
    EXPONENTIAL = 1
    TRIANGULAR = 2


def generate_uniform(rng, n):
    u = rng.random(n)
    return ALPHA * u


def generate_exponential(rng, n):
    u = rng.random(n)
    u = np.maximum(u, np.finfo(float).tiny)  # log(0) не определён
    return -np.log(u) / LAMBDA


def generate_triangular(rng, n):
    u = rng.random(n)
    return A * (1 - np.sqrt(u))


def uniform_density(x):
    return np.where((0 <= x) & (x <= ALPHA), 1 / ALPHA, 0)


def exponential_density(x):
    return np.where(x >= 0, LAMBDA * np.exp(-LAMBDA * x), 0)


def triangular_density(x):
    return np.where((0 <= x) & (x <= A), 2 * (A - x) / A**2, 0)


def generate_samples(distribution, rng, n):
    generators = {
        Distribution.UNIFORM: generate_uniform,
        Distribution.EXPONENTIAL: generate_exponential,
        Distribution.TRIANGULAR: generate_triangular,
    }
    return generators[distribution](rng, n)


def theoretical_density(distribution, x):
    densities = {
        Distribution.UNIFORM: uniform_density,
        Distribution.EXPONENTIAL: exponential_density,
        Distribution.TRIANGULAR: triangular_density,
    }
    return densities[distribution](x)


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    distributions = [Distribution.UNIFORM, Distribution.EXPONENTIAL, Distribution.TRIANGULAR]
    rng = np.random.default_rng(SEED)

    all_samples = {n: [generate_samples(d, rng, n) for d in distributions] for n in SAMPLE_SIZES}
    theory_means = [ALPHA / 2, 1 / LAMBDA, A / 3]
    theory_stds = [ALPHA / np.sqrt(12), 1 / LAMBDA, A / np.sqrt(18)]
    filenames = ["practice1_uniform.png", "practice1_exponential.png", "practice1_triangular.png"]
    names = ["Равномерное", "Показательное", "Треугольное"]
    max_x_values = [ALPHA, max(6 / LAMBDA, max(all_samples[n][Distribution.EXPONENTIAL].max() for n in SAMPLE_SIZES)), A]


    for distribution in distributions:
        theory_mean = theory_means[distribution]
        theory_std = theory_stds[distribution]
        max_x = max_x_values[distribution]
        filename = filenames[distribution]
        name = names[distribution]

        x = np.linspace(0, max_x, 600)
        y = theoretical_density(distribution, x)
        edges = np.linspace(0, max_x, 21)  # одинаковые интервалы внутри одного закона
        
        fig, axes = plt.subplots(1, 3, figsize=(15, 4.5), sharey=True)

        print(name)
        for ax, n in zip(axes, SAMPLE_SIZES):
            samples = all_samples[n][distribution]
            mean = np.mean(samples)
            std = np.std(samples, ddof=0)
            
            print(f"N={n:5d}")
            print(f"    M:   теория={theory_mean:8.3f}, модель={mean:8.3f}")
            print(f"    СКО: теория={theory_std:8.3f}, модель={std:8.3f}")

            ax.hist(samples, bins=edges, density=True, color="#a9c7e8",
                    edgecolor="#415e7c", alpha=0.8, label="Гистограмма")
            ax.plot(x, y, color="#c43e43", linewidth=2.2, linestyle='--',
                    label="Теоретическая плотность")
            ax.set_title(f"N = {n}")
            ax.set_xlabel("Значение случайной величины")
            ax.grid(alpha=0.2)
            ax.legend(fontsize=9)

        axes[0].set_ylabel("Плотность вероятности")
        fig.suptitle(f"{name} распределение", fontsize=15)
        fig.tight_layout()
        path = OUTPUT_DIR / filename
        fig.savefig(str(path), dpi=160, bbox_inches="tight")
        print(f"\n    Сохранено: {path.name}")

    plt.show()


if __name__ == "__main__":
    main()
