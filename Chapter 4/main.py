import tkinter as tk
from tkinter import filedialog
import time
from peptide_sequencing import BranchAndBoundCyclopeptide, LeaderboardAndConvolutionCyclopeptide, TheoreticalSpectra

def get_user_inputs():
    sequence = input("Enter amino acid sequence: ").strip()
    if not sequence:
        print("No peptide entered. Using default 'MEVPLSPIGT'.")
        sequence = "MEVPLSPIGT"
    sequence = sequence.upper()
    p_input = input("Enter P (default 0.1): ").strip()
    n_input = input("Enter N (default 25): ").strip()
    m_input = input("Enter M (default 20): ").strip()
    t_input = input("Enter T (default 0.5): ").strip()
    c_input = input("Enter C (default 1.0): ").strip()
    p = int(p_input) if p_input else 0.1
    n = int(n_input) if n_input else 25
    m = int(m_input) if m_input else 20
    t = float(t_input) if t_input else 0.5
    c = float(c_input) if c_input else 1.0
    return sequence, p, n, m, t, c
    
def main():
    sequence, p, n, m, t, c = get_user_inputs()
    ts = TheoreticalSpectra(p=0.0)
    theoretical_spectrum = ts.cyclic_spectrum_with_error(sequence, 0.0)
    error_spectrum = ts.cyclic_spectrum_with_error(sequence, p)
    algorithms = [
        ('Branch and Bound Cyclopeptide Sequencing', BranchAndBoundCyclopeptide()),
        ('Leaderboard Cyclopeptide Sequencing with Convolution', LeaderboardAndConvolutionCyclopeptide(n, m, t, c))
    ]
    results = [
        "Theoretical Spectrum:\n",
        f"{' '.join(map(str, theoretical_spectrum))}\n\n",
        f"Error-Simulated Spectrum (P={p:.2f}):\n",
        f"{' '.join(map(str, error_spectrum))}\n\n"
    ]
    overall_start = time.time()
    for algo_name, algo in algorithms:
        start_time = time.time()
        results.append(f"--- {algo_name} ---\n")
        if algo_name == 'Branch and Bound Cyclopeptide Sequencing':
            peptide = algo.run(' '.join(map(str, theoretical_spectrum)))
        else:
            peptide = algo.run(' '.join(map(str, error_spectrum)))
            score = algo.score(peptide, error_spectrum)
            results.append(f"Score: {score}\n")
        runtime = time.time() - start_time
        results.append(f"Runtime: {runtime:.1f} seconds\n")
        results.append(f"Peptide: {peptide}\n")
        results.append("\n")
    total_runtime = time.time() - overall_start
    results.append(f"Total Runtime: {total_runtime:.1f} seconds\n")
    with open('results.txt', 'w') as f:
        f.writelines(results)
    print("Results written to results.txt.")
    print(f"Total Runtime: {total_runtime:.1f} seconds")

if __name__ == "__main__":
    main()