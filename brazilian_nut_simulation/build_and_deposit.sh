maturin build
pip install --force-reinstall target/wheels/*.whl --target target/output/
mv target/output/*.whl ../