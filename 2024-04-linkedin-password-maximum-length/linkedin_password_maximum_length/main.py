import argparse
import argon2
import secrets
import string
import sys
import time

####################
# Argument parsing #
####################

parser = argparse.ArgumentParser(description="Benchmark long password with Argon2id.")
parser.add_argument(
    "--password-length", type=int, default=50
)
args = parser.parse_args(sys.argv[1:])

#######################
# Password generation #
#######################

character_choices = string.ascii_letters + string.digits + string.punctuation
password = ''.join(secrets.choice(character_choices) for i in range(args.password_length))

#####################
# Hash benchmarking #
#####################

start = time.time()

password_hasher = argon2.PasswordHasher.from_parameters(argon2.profiles.RFC_9106_LOW_MEMORY)
hashed_password = password_hasher.hash(password)

end = time.time()

##########
# Output #
##########

diff_in_ms = round((end - start)*1000)

print('Password length: ' + str(len(password)))
print('Hash:            ' + hashed_password)
print('Elapsed time:    ' + str(diff_in_ms) + "ms")
