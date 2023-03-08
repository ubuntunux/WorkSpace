def version_comp(v1, v2):
    ver1 = map(int, split(v1, '.'))
    ver2 = map(int, split(v2, '.'))
    
version_comp("0.0.2", "0.0.1")
version_comp("1.0.10", "1.0.3")
version_comp("1.2.0", "1.1.99")
version_comp("1.1", "1.0.1")
