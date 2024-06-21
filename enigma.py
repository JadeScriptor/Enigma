class Rotor:
    def __init__(self, wiring, notch):
        self.wiring = wiring
        self.notch = notch
        self.position = 0

    def set_position(self, position):
        self.position = position

    def forward(self, char):
        index = (ord(char) - ord('A') + self.position) % 26
        return chr((ord(self.wiring[index]) - ord('A') - self.position) % 26 + ord('A'))

    def backward(self, char):
        index = (self.wiring.index(chr((ord(char) - ord('A') + self.position) % 26 + ord('A'))) - self.position) % 26
        return chr(index + ord('A'))

    def rotate(self):
        self.position = (self.position + 1) % 26
        return self.position == ord(self.notch) - ord('A')

class Reflector:
    def __init__(self, wiring):
        self.wiring = wiring

    def reflect(self, char):
        return self.wiring[ord(char) - ord('A')]

class Plugboard:
    def __init__(self, wiring):
        self.wiring = {}
        for pair in wiring:
            self.wiring[pair[0]] = pair[1]
            self.wiring[pair[1]] = pair[0]

    def swap(self, char):
        return self.wiring.get(char, char)

class EnigmaMachine:
    def __init__(self, rotors, reflector, plugboard):
        self.rotors = rotors
        self.reflector = reflector
        self.plugboard = plugboard

    def set_positions(self, positions):
        for rotor, position in zip(self.rotors, positions):
            rotor.set_position(position)

    def encrypt_decrypt(self, text):
        encrypted_text = ""
        for char in text:
            if char.isalpha():
                char = char.upper()
                char = self.plugboard.swap(char)
                for rotor in self.rotors:
                    char = rotor.forward(char)
                char = self.reflector.reflect(char)
                for rotor in reversed(self.rotors):
                    char = rotor.backward(char)
                char = self.plugboard.swap(char)
                encrypted_text += char

                # Rotate the rotors
                for i, rotor in enumerate(self.rotors):
                    if not rotor.rotate():
                        break
            else:
                encrypted_text += char
        return encrypted_text

# Contoh penggunaan
rotor1 = Rotor("EKMFLGDQVZNTOWYHXUSPAIBRCJ", "Q")
rotor2 = Rotor("AJDKSIRUXBLHWTMCQGZNPYFVOE", "E")
rotor3 = Rotor("BDFHJLCPRTXVZNYEIWGAKMUSQO", "V")
reflector = Reflector("YRUHQSLDPXNGOKMIEBFZCWVJAT")
plugboard = Plugboard([("A", "B"), ("C", "D"), ("E", "F")])

enigma = EnigmaMachine([rotor1, rotor2, rotor3], reflector, plugboard)
enigma.set_positions([0, 0, 0])

# Encrypt process
message = "HELLO"
encrypted_message = enigma.encrypt_decrypt(message)
print("Encrypted Message:", encrypted_message)

# Decrypt process
enigma.set_positions([0, 0, 0])
decrypted_message = enigma.encrypt_decrypt(encrypted_message)
print("Decrypted Message:", decrypted_message)
