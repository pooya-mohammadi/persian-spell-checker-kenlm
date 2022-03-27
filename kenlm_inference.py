import kenlm

model = kenlm.Model('fa_wiki.binary')
print("score: ", model.score("تهران سهر است.", bos=True, eos=True))  # score: -17.82791519165039
print("score: ", model.score('تهران شهر است.', bos=True, eos=True))  # score: -14.51852035522461
print("score: ", model.score("تهران سهر است.", bos=False, eos=True))  # score: -17.287336349487305
print("score: ", model.score('تهران شهر است.', bos=False, eos=True))  # score: -14.971918106079102
print("score: ", model.score("تهران سهر است.", bos=False, eos=False))  # score: -15.25560188293457
print("score: ", model.score('تهران شهر است.', bos=False, eos=False))  # score: -12.940183639526367
print("score: ", model.score("تهران سهر است.", bos=True, eos=False))  # score: -15.796180725097656
print("score: ", model.score('تهران شهر است.', bos=True, eos=False))  # score: -12.486785888671875
