import numpy as np
import yaml
import os

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

def processFile(file_path, output_file="eigvec4.dat", fac=241.7991, eig_index=3):
    if not os.path.exists(file_path):
        return print(f"Error: {file_path} not found.")
    
    try:
        with open(file_path, "r") as stream:
            phonon = yaml.load(stream, Loader=Loader)
            bands = np.array(phonon['phonon'][0]['band'])
            frequencies = np.array([band['frequency'] for band in bands])
            eigenvectors = np.array([band['eigenvector'] for band in bands])
    except Exception as e:
        
        return print(f"Error processing file: {e}")

    print("\n".join([f"{f/fac*1000:.3g} meV" for f in frequencies]))
    print(f"Eigenvector shape: {eigenvectors.shape}")

    try:
        with open(output_file, "w") as f:
            for vec in eigenvectors[eig_index]:
                vxr, vxi, vyr, vyi, vzr, vzi = vec.reshape(6)
                print(f"{vxr:.4f} {vyr:.4f} {vzr:.4f}")
                f.write(f"{vxr:.8f} {vyr:.8f} {vzr:.8f}\n")
        print(f"Eigenvector saved to {output_file}")
        
    except Exception as e:
        print(f"Error saving eigenvector: {e}")

if __name__ == "__main__":
    processFile("qpoints.yaml")
