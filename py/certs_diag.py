#!/usr/bin/env python3 
#     """show certificates tree in json"""

import typer
import json
from pathlib import Path
from typing import List, Dict
from qutil.log.log import setup_logger
from loguru import logger 
from cryptography import x509
from cryptography.x509  import load_pem_x509_certificates, load_der_x509_certificate
from cryptography.hazmat.primitives.asymmetric import rsa, ec
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature
from collections import defaultdict

setup_logger()

def verify_cert_signature(issuer_cert, subject_cert):
    public_key = issuer_cert.public_key()
    try:
        logger.debug(f"Verifying signature for {subject_cert.subject} issued by {issuer_cert.subject}")
        if isinstance(public_key, rsa.RSAPublicKey):
            # Most RSA signatures use PKCS1v15 padding
            logger.debug(f"Using RSA public key for verification")
            public_key.verify(
                subject_cert.signature,
                subject_cert.tbs_certificate_bytes,
                padding.PKCS1v15(),
                subject_cert.signature_hash_algorithm,
            )
        elif isinstance(public_key, ec.EllipticCurvePublicKey):
            # ECDSA uses no padding, just hash algorithm
            logger.debug(f"Using elliptic curve public key for verification")
            public_key.verify(
                subject_cert.signature,
                subject_cert.tbs_certificate_bytes,
                ec.ECDSA(subject_cert.signature_hash_algorithm)
            )
        else:
            # Other key types can be added here
            raise ValueError("Unsupported public key type")
    except InvalidSignature:
        logger.error(f"Invalid signature for {subject_cert.subject} issued by {issuer_cert.subject}")
        return False
    return True
  
def is_issuer(parent, child):
    # Step 1: check issuer == subject

    if child.issuer != parent.subject:
        return False
    # Step 2: verify signature 

    logger.debug(f"subject and issuer match")
    if not verify_cert_signature(parent, child):
        return False
    logger.debug(f"Signature verified successfully")
    return True
   
def load_certificates(cert_path: Path) -> x509.Certificate:
    """Load a certificate from a file."""
    with open(cert_path, 'rb') as f:
        cert_data = f.read()
    try:
        return load_pem_x509_certificates(cert_data)
    except ValueError:
        return load_der_x509_certificate(cert_data) 

def find_certificate_files(dir_path: Path) -> List[Path]:
    """Find all certificate files in a directory."""
    cert_files = []
    for path in dir_path.rglob('*'):
        if path.is_file() and path.suffix in ['.pem', '.crt', '.cer']:
            cert_files.append(path)
            logger.info(f"Found certificate file: {path}")
    return cert_files

def find_certificate_files_from_dirs(dirs: List[Path]) -> List[Path]:
    """Find all certificate files in a list of directories."""
    if isinstance(dirs, Path):
        dirs = [dirs] 
    cert_files = []
    for dir_path in dirs:
        if dir_path.is_dir():
            cert_files.extend(find_certificate_files(dir_path))
        else:
            logger.warning(f"Path is not a directory: {dir_path}")
    return cert_files  
  

def load_certficates_from_dirs(dir_path: list[Path]) -> Dict[x509.Certificate, List[str]]:
    """Load all certificates from a list of directory."""
    certs = {}
    files = find_certificate_files_from_dirs(dir_path)
    for file_path in files:
        try:
            # one file could have mutliple certificates
            certs_from_file = load_certificates(file_path)
            for c in certs_from_file: 
                if c in certs:
                    certs[c].append(file_path.as_posix())
                else:
                    certs[c] = [file_path.as_posix()] 
        except Exception as e:
            logger.error(f"Failed to load certificate from {file_path}: {e}")
    return certs
 
def build_cert_forest(cert_dict):
    # Build parent-child relationships using is_issuer
    '''children_map is dict structure:
    {
        parent_path: [child_path1, child_path2, ...],
        ...
    }
    '''
    children_map = defaultdict(list)
    roots = []

    cert_items = list(cert_dict.items())
    # For each cert, find its parent by is_issuer
    for child_cert, child_path in cert_items:
        parent_found = False
        for parent_cert, parent_path in cert_items:
            if parent_cert == child_cert:
                continue
            if is_issuer(parent_cert, child_cert):
                children_map[parent_cert].append(child_cert)
                parent_found = True
                break
        if not parent_found:
            roots.append(child_cert)

    # Tree node = {path, certificate, children: [...]}
    def build_tree(cert):
        return {
            "certificate": cert,
            "path": cert_dict[cert],
            "children": [build_tree(child) for child in children_map.get(cert, [])]
        }

    return [build_tree(root) for root in roots]

app = typer.Typer()  # Default help enabled

@app.callback()
def main(
    debug: bool = typer.Option(False, "--debug", help="Enable debug logging")
):
    """Global options for the CLI."""
    if debug:
        setup_logger(console_log=True, level="DEBUG")
        logger.debug("Debug logging enabled.")

@app.command()
def show_forest(
    dirs: List[Path] = typer.Argument(..., help="List of directories containing certificates")
):
    """
    Load certificates from given directories and show the certificate forest as JSON.
    """
    certs = load_certficates_from_dirs(dirs)
    logger.debug(f"Loaded {len(certs)} certificates from directories: {dirs} \n")

    forest = build_cert_forest(certs)
    # Convert certificates to strings for JSON serialization
    def cert_tree_to_dict(node):
        return {
            "certificate": str(node["certificate"]), 
            "path": node["path"],
            "children": [cert_tree_to_dict(child) for child in node["children"]]
        }
    forest_dict = [cert_tree_to_dict(root) for root in forest]
    typer.echo(json.dumps(forest_dict, indent=2))



@app.command()
def show_certs(
    dirs: List[Path] = typer.Argument(..., help="List of directories containing certificates")
):
    """
    Load certificates from given directories and show the certificate details.
    """
    certs = load_certficates_from_dirs(dirs)
    logger.debug(f"Loaded {len(certs)} certificates from directories: {dirs} \n")
    data = []
    for cert, cert_path in certs.items():
        data.append({
            "certificate": str(cert),
            "path": cert_path
        })

    typer.echo(json.dumps(data, indent=2))


if __name__ == "__main__":
    app()



