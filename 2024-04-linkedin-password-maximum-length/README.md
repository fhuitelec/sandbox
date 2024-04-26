# Password maximum length standards

This Python script benchmarks `argon2id` with a recommended profile in a CPU constrained setup to verify how password length impacts hashing time.

## The question

ANSSI's (french security government agency) and CNIL's (french regulatory commission for data privacy) recommandations both recommend setting a few hundred characters maximum length.

> **From a Denial of Service (DoS) perspective, is this recommandation safe?**

## Results

> **TL;DR: yes, a few hundreds character maximum length is safe for password hash comparison using argon2id**.

| Password length                        | Time   |
| -------------------------------------- | ------ |
| 10                                     | 1085ms |
| 20                                     | 1005ms |
| 50                                     | 997ms  |
| 100                                    | 1108ms |
| 200                                    | 1001ms |
| 500                                    | 1188ms |
| 1 000                                  | 1101ms |
| 5 000                                  | 1101ms |
| 10 000                                 | 1091ms |
| 100 000                                | 1103ms |
| 1 000 000                              | 1001ms |
| 1 000 000 000<sup>1</sup> <sup>2</sup> | 9004ms |

<sup>1</sup> Generating the password was done with a variant of the current script in a non CPU-constraint environment with multiple threads (still using Python's [secrets](https://docs.python.org/3/library/secrets.html) module) resulting in a 1GB password.

<sup>2</sup> Note that with 1 billion characters, we are not far from the ~4 billions maximum input limit of argon2! The result is quite impressive.

## Usage

```
usage: main.py [-h] [--password-length PASSWORD_LENGTH]

Benchmark long password with Argon2id.

options:
  -h, --help            show this help message and exit
  --password-length PASSWORD_LENGTH
```

Using the docker setup:

```shell
# Build the image
docker build -t fhuitelec/argon2id-benchmark .

# Run it 
docker run -ti --cpus=0.25 fhuitelec/argon2id-benchmark --password-length=200
```

## `argon2id`

### Why

Because, as of april, 2024 this is [OWASP's recommandation](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html).

### Library

We use Python's [`argon2-ffi`](https://pypi.org/project/argon2-cffi/) as:
- it is listed in [Password Hashing Competition's bindings](https://github.com/p-h-c/phc-winner-argon2?tab=readme-ov-file#bindings)
- it is the most used library (500+ stars)
- it is the most maintained  library (latest commit 10 days ago)
- its API is well designed and well documented

### Parameters

As per `argon2-ffi`'s [suggestion](https://argon2-cffi.readthedocs.io/en/stable/parameters.html), we use [RFC 9106's](https://www.rfc-editor.org/rfc/rfc9106.html) second recommended option (destined for low memory execution environment):

- time cost: 3 iterations
- parallelism: 4 lanes
- memory cost: 64 MiB
- salt length: 128 bits
- hash size: 256 bits

### CPU constraint

We use Docker's [resource constraints](https://docs.docker.com/config/containers/resource_constraints/#cpu) by throttling above 0,25 CPUs.

## Sources

- (🇫🇷) [ANSSI's Recommendations relating to multi-factor authentication and to passwords v2](https://cyber.gouv.fr/sites/default/files/2021/10/anssi-guide-authentification_multifacteur_et_mots_de_passe.pdf) ()
  - published on 2021/10/08
  - see section R22 p. 29
- (🇫🇷) [CNIL's Deliberation No. 2022-100 adopting recommendations regarding passwords and other shared secrets](https://www.cnil.fr/sites/cnil/files/atoms/files/deliberation-2022-100-du-21-juillet-2022_recommandation-aux-mots-de-passe.pdf)
  - published on 2022/07/21
  - see bullet point #31 p. 7
- (🇬🇧) [RFC 9106](https://www.rfc-editor.org/rfc/rfc9106.html)
- (🇬🇧) [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
- (🇬🇧) [`argon2-ffi` Choosing parameters](https://argon2-cffi.readthedocs.io/en/stable/parameters.html)
- (🇬🇧) [`argon2-ffi` API reference](https://argon2-cffi.readthedocs.io/en/stable/api.html)
- (🇬🇧) [Password Hashing Competition's bindings](https://github.com/p-h-c/phc-winner-argon2?tab=readme-ov-file#bindings)
