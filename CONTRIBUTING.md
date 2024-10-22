### 🛠 How to Contribute

We welcome your contributions to the `Puppys` framework! Here’s a quick guide to get started:

### Steps:
1. **Fork**: Fork the repository and clone it locally.
    ```bash
    git clone https://github.com/PuppyAgent/Puppys.git
    ```
2. **Create a Branch**: Make a feature branch to work on:
    ```bash
    git checkout -b feature/your-feature
    ```
3. **Code**: Develop your feature or fix.
4. **Commit**: Write clear commit messages and commit your changes.
    ```bash
    git commit -m "Add feature XYZ"
    ```
5. **Push**: Push the changes to your fork.
    ```bash
    git push origin feature/your-feature
    ```
6. **PR**: Open a Pull Request to the main repository and include a brief description of the changes.

### Pull Request Guidelines:
- PRs should be for **one feature or fix** only.
- Link relevant issues (e.g., `Closes #123`).
- Ensure tests are written and pass.
- Be open to feedback and revise accordingly.
- Reserved for stable releases. Do not push directly to the **`main`** or **`qubits`** branch.

### Rules:
- **Code Style**: Follow consistent naming and formatting (see below for styles).
- **Documentation**: Update relevant docs for any new features.
- **Tests**: Ensure your code is tested before submission.

---

### 🚀 Code Writing Rules & Styles

Based on the provided code, here are some guidelines for writing clean and maintainable code:

1. **Type Hinting**: Use Python type annotations to improve code readability. Make sure to write each arg into separate lines:
   - Example: 
   ```python
   def add(
        self,
        arg1: int,
        arg2: str
    ) -> None:
        pass
   ```

2. **Docstrings**: Use descriptive and concise docstrings to explain classes, methods, and arguments.
   - Format:
     ```python
     """
     Description

     Args:
         Name (Data Type, optional): Description. (Defaults to XXX.)
    
     Returns:
         Name (Data Type): Description.
     """
     ```

3. **Error Handling**: Include clear error messages when raising exceptions.

4. **Encapsulation**: Encapsulate environment data using getter methods and restrict direct attribute modification (e.g., private variables like `private_keys`).

5. **Avoid Redundancy**: Use helper methods or loops to avoid repeating code when processing similar tasks, such as dynamically loading attributes.
