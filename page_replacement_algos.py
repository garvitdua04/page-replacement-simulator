import matplotlib.pyplot as plt
import random
import time

class PageReplacementSimulator:
    def fifo_replacement(self, reference_string, frame_count):
        """
        First-In-First-Out (FIFO) page replacement algorithm implementation

        Args:
            reference_string: List of page references
            frame_count: Number of frames available

        Returns:
            page_faults: Number of page faults
            frames_history: List of frame states at each step
        """
        frames = []
        page_faults = 0
        frames_history = []

        for i, page in enumerate(reference_string):
            # Save current frame state
            frames_history.append(frames.copy())

            if page not in frames:
                page_faults += 1
                if len(frames) < frame_count:
                    frames.append(page)
                else:
                    # Replace the oldest page (first in the list)
                    frames.pop(0)
                    frames.append(page)

        # Save final frame state
        frames_history.append(frames.copy())

        return page_faults, frames_history

    def lru_replacement(self, reference_string, frame_count):
        """
        Least Recently Used (LRU) page replacement algorithm implementation

        Args:
            reference_string: List of page references
            frame_count: Number of frames available

        Returns:
            page_faults: Number of page faults
            frames_history: List of frame states at each step
        """
        frames = []
        page_faults = 0
        frames_history = []

        # Keep track of recently used pages with their timestamps
        usage_history = {}

        for i, page in enumerate(reference_string):
            # Save current frame state
            frames_history.append(frames.copy())

            # Update the timestamp for this page
            usage_history[page] = i

            if page not in frames:
                page_faults += 1
                if len(frames) < frame_count:
                    frames.append(page)
                else:
                    # Find the least recently used page
                    lru_page = None
                    oldest_timestamp = float('inf')

                    for frame_page in frames:
                        if usage_history[frame_page] < oldest_timestamp:
                            oldest_timestamp = usage_history[frame_page]
                            lru_page = frame_page

                    # Replace the LRU page
                    frames.remove(lru_page)
                    frames.append(page)

        # Save final frame state
        frames_history.append(frames.copy())

        return page_faults, frames_history

    def optimal_replacement(self, reference_string, frame_count):
        """
        Optimal page replacement algorithm implementation

        Args:
            reference_string: List of page references
            frame_count: Number of frames available

        Returns:
            page_faults: Number of page faults
            frames_history: List of frame states at each step
        """
        frames = []
        page_faults = 0
        frames_history = []

        for i, page in enumerate(reference_string):
            # Save current frame state
            frames_history.append(frames.copy())

            if page not in frames:
                page_faults += 1
                if len(frames) < frame_count:
                    frames.append(page)
                else:
                    # Find the page that will not be used for the longest time
                    future_usage = {}

                    for frame_page in frames:
                        # Find the next occurrence of this page
                        try:
                            next_index = reference_string[i+1:].index(frame_page) + i + 1
                            future_usage[frame_page] = next_index
                        except ValueError:
                            # If the page doesn't appear in the future, set to infinity
                            future_usage[frame_page] = float('inf')

                    # Find the page with the furthest next use (or never used again)
                    replace_page = max(future_usage.items(), key=lambda x: x[1])[0]
                    frames.remove(replace_page)
                    frames.append(page)

        # Save final frame state
        frames_history.append(frames.copy())

        return page_faults, frames_history

    def print_trace(self, algorithm, reference_string, frames_history):
        """Print detailed execution trace of the algorithm"""
        print(f"\n===== {algorithm} Page Replacement Trace =====")
        print("Reference String:", reference_string)
        print("\nStep | Page | Frames | Page Fault")
        print("-" * 50)

        for i, page in enumerate(reference_string):
            frames_before = frames_history[i]
            frames_after = frames_history[i+1]

            is_fault = page not in frames_before
            fault_marker = "Yes" if is_fault else "No"

            print(f"{i+1:4} | {page:4} | {str(frames_after):20} | {fault_marker}")

    def compare_algorithms(self, reference_string, frame_count):
        """Compare the performance of all three algorithms"""
        # Run all algorithms
        fifo_faults, fifo_history = self.fifo_replacement(reference_string, frame_count)
        lru_faults, lru_history = self.lru_replacement(reference_string, frame_count)
        optimal_faults, optimal_history = self.optimal_replacement(reference_string, frame_count)

        # Print traces if needed
        self.print_trace("FIFO", reference_string, fifo_history)
        self.print_trace("LRU", reference_string, lru_history)
        self.print_trace("Optimal", reference_string, optimal_history)

        # Print comparison results
        print("\n===== Performance Comparison =====")
        print(f"Reference String: {reference_string}")
        print(f"Frame Count: {frame_count}")
        print("\nAlgorithm | Page Faults | Fault Rate | Hit Rate")
        print("-" * 60)

        print(f"FIFO     | {fifo_faults:11} | {(fifo_faults / len(reference_string)) * 100:9.2f}% | {(1 - (fifo_faults / len(reference_string))) * 100:8.2f}%")
        print(f"LRU      | {lru_faults:11} | {(lru_faults / len(reference_string)) * 100:9.2f}% | {(1 - (lru_faults / len(reference_string))) * 100:8.2f}%")
        print(f"Optimal  | {optimal_faults:11} | {(optimal_faults / len(reference_string)) * 100:9.2f}% | {(1 - (optimal_faults / len(reference_string))) * 100:8.2f}%")

        # Create and show bar chart
        self.plot_comparison(reference_string, frame_count, fifo_faults, lru_faults, optimal_faults)

        return {
            'FIFO': fifo_faults,
            'LRU': lru_faults,
            'Optimal': optimal_faults
        }

    def plot_comparison(self, reference_string, frame_count, fifo_faults, lru_faults, optimal_faults):
        """Create a bar chart comparing algorithm performance"""
        algorithms = ['FIFO', 'LRU', 'Optimal']
        page_faults = [fifo_faults, lru_faults, optimal_faults]

        plt.figure(figsize=(10, 6))
        bars = plt.bar(algorithms, page_faults, color=['blue', 'green', 'red'])

        # Add the values on top of the bars
        for i, v in enumerate(page_faults):
            plt.text(i, v + 0.1, str(v), ha='center')

        plt.ylabel('Number of Page Faults')
        plt.title(f'Page Replacement Algorithm Comparison (Frame Size: {frame_count})')

        plt.tight_layout()
        plt.savefig(f"page_replacement_comparison_{frame_count}_frames.png")
        plt.show()

    def test_with_different_frame_sizes(self, reference_string, frame_sizes):
        """Test all algorithms with different frame sizes and detect Belady's anomaly"""
        results = {
            'FIFO': [],
            'LRU': [],
            'Optimal': []
        }

        for frame_count in frame_sizes:
            print(f"\n\n===== Testing with {frame_count} frames =====")
            comparison = self.compare_algorithms(reference_string, frame_count)

            for algorithm, faults in comparison.items():
                results[algorithm].append(faults)

        # Plot frame size comparison
        plt.figure(figsize=(10, 6))

        plt.plot(frame_sizes, results['FIFO'], 'o-', label='FIFO', color='blue')
        plt.plot(frame_sizes, results['LRU'], 's-', label='LRU', color='green')
        plt.plot(frame_sizes, results['Optimal'], '^-', label='Optimal', color='red')

        for i, size in enumerate(frame_sizes):
            plt.text(size, results['FIFO'][i] + 0.1, str(results['FIFO'][i]), ha='center')
            plt.text(size, results['LRU'][i] + 0.1, str(results['LRU'][i]), ha='center')
            plt.text(size, results['Optimal'][i] + 0.1, str(results['Optimal'][i]), ha='center')

        plt.xlabel('Frame Size')
        plt.ylabel('Number of Page Faults')
        plt.title('Page Faults vs Frame Size')
        plt.xticks(frame_sizes)
        plt.legend()

        plt.tight_layout()
        plt.savefig("frame_size_comparison.png")
        plt.show()

        # Check for Belady's anomaly in FIFO
        for i in range(1, len(frame_sizes)):
            if results['FIFO'][i] > results['FIFO'][i-1]:
                print(f"\nBelady's Anomaly detected in FIFO: Increasing frames from {frame_sizes[i-1]} to {frame_sizes[i]} increased page faults from {results['FIFO'][i-1]} to {results['FIFO'][i]}")

# Test data generation
def generate_test_data():
    """Generate various reference string patterns for testing"""
    # Standard test case
    standard_test = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1]

    # Sequential access pattern
    sequential_test = list(range(10))

    # Random access pattern
    random.seed(42)  # For reproducibility
    random_test = [random.randint(0, 9) for _ in range(20)]

    # Locality-based pattern
    locality_test = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5, 3, 4, 5, 6, 7, 6, 7, 8]

    # Loop pattern
    loop_test = [1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5]

    # Belady's anomaly example for FIFO
    belady_test = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]

    return {
        "Standard Test": standard_test,
        "Sequential": sequential_test,
        "Random": random_test,
        "Locality-Based": locality_test,
        "Loop Pattern": loop_test,
        "Belady's Test": belady_test
    }

# Main program execution
def main():
    # Create simulator instance
    simulator = PageReplacementSimulator()

    # Generate test data
    test_data = generate_test_data()

    # Test standard reference string with 3 frames
    print("\n===== STANDARD TEST CASE =====")
    reference_string = test_data["Standard Test"]
    simulator.compare_algorithms(reference_string, 3)

    # Test with different frame sizes (checking for Belady's anomaly)
    print("\n===== TESTING WITH DIFFERENT FRAME SIZES =====")
    simulator.test_with_different_frame_sizes(reference_string, [3, 4, 5])

    # Test different access patterns
    print("\n===== TESTING DIFFERENT ACCESS PATTERNS =====")
    for name, pattern in test_data.items():
        if name != "Standard Test":  # Already tested above
            print(f"\n----- {name} Pattern -----")
            simulator.compare_algorithms(pattern, 3)

    # Specifically test for Belady's anomaly with known problematic sequence
    print("\n===== TESTING FOR BELADY'S ANOMALY =====")
    simulator.test_with_different_frame_sizes(test_data["Belady's Test"], [3, 4, 5])

    print("\nAll tests completed. Performance comparison charts have been generated.")

if __name__ == "__main__":
    main()