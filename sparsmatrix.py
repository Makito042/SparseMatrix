class SparseMatrix:
    def __init__(self, filename):
        """Initialize the sparse matrix by loading it from a file."""
        self.matrix = self.load_sparse_matrix(filename)

    def load_sparse_matrix(self, filename):
        """Reads a sparse matrix from a file in the specified format."""
        with open(filename, 'r') as file:
            rows, cols = [int(file.readline().strip().split('=')[1]) for _ in range(2)]
            matrix = [[0] * cols for _ in range(rows)]
            for line in file:
                if line.strip():
                    try:
                        r, c, v = [int(x) for x in line.strip()[1:-1].split(',')]
                        matrix[r - 1][c - 1] = v
                    except ValueError:
                        raise ValueError("Incorrect format in input file.")
        return matrix

    def perform_operation(self, other_matrix, operation):
        """Performs addition, subtraction, or multiplication with another matrix."""
        if len(self.matrix) != len(other_matrix.matrix) or len(self.matrix[0]) != len(other_matrix.matrix[0]):
            raise ValueError("Matrices must have compatible dimensions.")

        result = [[0] * len(other_matrix.matrix[0]) for _ in range(len(self.matrix))]

        for i in range(len(self.matrix)):
            for j in range(len(other_matrix.matrix[0])):
                if operation == 'add':
                    result[i][j] = self.matrix[i][j] + other_matrix.matrix[i][j]
                elif operation == 'subtract':
                    result[i][j] = self.matrix[i][j] - other_matrix.matrix[i][j]
                elif operation == 'multiply':
                    for k in range(len(other_matrix.matrix)):
                        result[i][j] += self.matrix[i][k] * other_matrix.matrix[k][j]

        return result

    @staticmethod
    def save_to_file(matrix, output_file):
        """Writes the matrix to a file in the specified format."""
        with open(output_file, 'w') as file:
            for i, row in enumerate(matrix):
                for j, val in enumerate(row):
                    if val != 0:  # Only write non-zero values
                        file.write(f"({i + 1}, {j + 1}, {val})\n")


def main():
    """Main function to handle user input and matrix operations."""
    try:
        file1 = input("Input the path of the first file: ")
        file2 = input("Input the path of the second file: ")
        operation = input("What operation do you want to perform [add, subtract, multiply]: ")
        output_file = input("What's the name of the output file: ") or f"matrix_{operation}.txt"

        matrix1 = SparseMatrix(file1)
        matrix2 = SparseMatrix(file2)

        if operation in ['add', 'subtract', 'multiply']:
            result = matrix1.perform_operation(matrix2, operation)
            print(f"Matrix {operation}:")
            SparseMatrix.save_to_file(result, output_file)
            print(f"Result saved to {output_file}")

        else:
            raise ValueError("Invalid operation")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()