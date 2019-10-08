import base64
import string


def Decrypt(krypteret_indhold, kodeord) :
	r = ''
	kodeordLen = len(kodeord)
	for i in range(0, len(krypteret_indhold)) :
		c = ord(krypteret_indhold[i]) ^ ord(kodeord[i % kodeordLen])
		r += chr(c)
	return r


def SanitizeOutput(decodet, muligeDekrypteredeTegn) :
	r = ''
	for c in decodet :
		if c in muligeDekrypteredeTegn :
			r += c
		else :
			r += '?'
	return r


# :: ----------------- Kode til at lave lidt statistik ----------------->


def BruteForceFoersteKodeordsTegn(krypteret_indhold, muligeKodeordsTegn, muligeDekrypteredeTegn) :
	fundneMuligeTegn = set()
	for c in muligeKodeordsTegn :
		d = Decrypt(krypteret_indhold, c)
		if d[0:1] in muligeDekrypteredeTegn :
			fundneMuligeTegn.add(c)

	print "Mulige tegn til foesrte kodeords tegn: ", len(fundneMuligeTegn), " : ", fundneMuligeTegn


# :: ----------------- Kode til at finde laengden paa kodeordet ----------------->


def GiverDekodningMeningMedLaengde(decodet, muligeDekrypteredeTegn, currentLength) :
	r = 0
	for i in range(0, len(decodet), currentLength):
		firstChar = decodet[i : i + 1]
		if firstChar not in muligeDekrypteredeTegn:
			return 0
		r += 1

	return r


def FindOrdMedBruteForceLoop(muligeKodeordsTegn, muligeDekrypteredeTegn, krypteret_indhold) :

	antalMulige = dict()

	for currentLength in range(1, 16) :
		for c1 in muligeKodeordsTegn :
			key = (c1 * currentLength)
			d = Decrypt(krypteret_indhold, key)

			r = GiverDekodningMeningMedLaengde(d, muligeDekrypteredeTegn, currentLength)
			if r == 0 :
				continue

			if not antalMulige.has_key(currentLength) :
				antalMulige[currentLength] = 0

			antalMulige[currentLength] += 1

	return antalMulige


# :: ----------------- Kode til at finde selve kodeordet ----------------->


def GiverDekodningMeningMedLaengdeMedDelta(decodet, muligeDekrypteredeTegn, currentLength, delta = 1) :
	r = 0
	for i in range(0, len(decodet), currentLength):

		for offset in range(0, delta):
			c = decodet[i + offset : i + offset + 1]
			if c not in muligeDekrypteredeTegn:
				return 0
			r += 1

	return r


def PrintKodeordHvertTrin(decodet, muligeDekrypteredeTegn, currentLength, delta = 1) :
	r = ''
	for i in range(0, len(decodet), currentLength):

		for offset in range(0, delta):
			c = decodet[i + offset: i + offset + 1]
			if c not in muligeDekrypteredeTegn:
				return 0
			r += c

	return r


def FindOrdMedBruteForceRekursiv(muligeKodeordsTegn, muligeDekrypteredeTegn, krypteret_indhold, currentLength, generatedLength, firstPart) :
	firstPartLen = len(firstPart)
	if currentLength == generatedLength + firstPartLen :
		key = firstPart + ("?" * generatedLength)

		assert(len(key) == currentLength)

		d = Decrypt(krypteret_indhold, key)
		r1 = GiverDekodningMeningMedLaengdeMedDelta(d, muligeDekrypteredeTegn, currentLength, firstPartLen)
		if r1 > 0:
			print key, " == ", PrintKodeordHvertTrin(d, muligeDekrypteredeTegn, currentLength, firstPartLen)

		return

	for c in muligeKodeordsTegn :
		key = firstPart + c
		FindOrdMedBruteForceRekursiv(muligeKodeordsTegn, muligeDekrypteredeTegn, krypteret_indhold, currentLength, generatedLength, key)


# :: ----------------- Main ----------------->


krypteret_indhold = base64.b64decode('Vg0TGwVSbVkQAQEQUG5WBxVIYysIAQZODgUPFg8RRnxVDhVbeCgJCAkBHkUCBFNMKSZBFQEMBQsOCw4YDjMGAy0FCg0LAA86Fx4ZMwUcBgsWFFIGGFttSgseWW9ODBdXZ25WSgUZDRVZb05BDR0DCFRv')

muligeKodeordsTegn = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-"

#muligeDekrypteredeTegn = string.ascii_letters + string.digits + "\n" + "<>!{}_:/ "
muligeDekrypteredeTegn = string.printable


print "Len:", len(krypteret_indhold)

BruteForceFoersteKodeordsTegn(krypteret_indhold, muligeKodeordsTegn, muligeDekrypteredeTegn)


antalMulige = FindOrdMedBruteForceLoop(muligeKodeordsTegn, muligeDekrypteredeTegn, krypteret_indhold)

print "Statistik: "
for k,v in antalMulige.items():
	print "Laengde:", k, "var ok", v, "gange"

highestV = 0
highestK = 0
for k,v in antalMulige.items() :
	if v > highestV :
		highestV = v
		highestK = k

print "Kodeordet er nok", highestK, "antal tegn langt ..."

d = Decrypt(krypteret_indhold, "a???")
r1 = ''
r2 = ''
for i in range(0, 15) :
	r1 += "|" + hex(ord(krypteret_indhold[i]))
	r2 += "|" + d[i]
print r1
print r2


antalTegnTilBruteForcing = 1
FindOrdMedBruteForceRekursiv(muligeKodeordsTegn, muligeDekrypteredeTegn, krypteret_indhold, highestK, highestK - antalTegnTilBruteForcing, "")

antalTegnTilBruteForcing = 2
FindOrdMedBruteForceRekursiv(muligeKodeordsTegn, muligeDekrypteredeTegn, krypteret_indhold, highestK, highestK - antalTegnTilBruteForcing, "j")

antalTegnTilBruteForcing = 3
FindOrdMedBruteForceRekursiv(muligeKodeordsTegn, muligeDekrypteredeTegn, krypteret_indhold, highestK, highestK - antalTegnTilBruteForcing, "je")

# osv.

#antalTegnTilBruteForcing = 14
#FindOrdMedBruteForceRekursiv(muligeKodeordsTegn, muligeDekrypteredeTegn, krypteret_indhold, highestK, highestK - antalTegnTilBruteForcing, "jegvilgernein")
