#include <cmath>
#include <iostream>
#include <map>
#include <string>

using namespace std;

double calculate_entropy(const string &text) {
    if (text.empty()) {
        return 0.0;
    }

    map<char, int> freq;
    for (char c : text) {
        freq[c]++;
    }

    double entropy = 0.0;
    for (const auto &pair : freq) {
        double p = static_cast<double>(pair.second) / text.size();
        entropy -= p * log2(p);
    }
    return entropy;
}

double calculate_redundancy(const string &text, int alphabet_size = 256) {
    // TODO(student): implement redundancy = log2(N) - H(X)
    // Hint: use calculate_entropy(text)
    (void)text;
    (void)alphabet_size;
    return -1.0;
}

int main() {
    string input;
    cout << "Enter a string of characters: ";
    getline(cin, input);

    double entropy = calculate_entropy(input);
    double redundancy = calculate_redundancy(input);

    cout << "Entropy: " << entropy << '\n';
    cout << "Redundancy: " << redundancy << '\n';
    return 0;
}
