maturin build
pip install --upgrade target/wheels/*.whl --target target/output/
mv target/output/brazilian_nut_simulation/*.so ../brazilian_nut_wrapper/src/brazilian_nut_wrapper