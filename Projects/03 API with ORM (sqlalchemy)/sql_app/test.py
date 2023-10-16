import utils


plain = "123"
hashed = utils.hash_function(plain)
x = utils.verify(plain, hashed)
print(plain)
print(hashed)
print(x)

"""eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9
eyJ1c2VyX2lkIjoxLCJleHAiOjE2OTczMTQ2NjV9
qSfDubgVnwXH4NQi2XFKLneXKm_u3JqxyH6yTH1zDSg"""