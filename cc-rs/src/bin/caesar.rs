use std::collections::HashMap;
use std::env;
use std::io::{self, BufRead};

static NA: &str = "NA";

fn main() -> io::Result<()> {
    let debug = env::var("DEBUG").is_ok();
    let mut buffer = String::new();
    let stdin = io::stdin();
    let mut handle = stdin.lock();
    let source_text = "abcdefghijklmnopqrstuvwxyz1234567890";
    let mut lookup = create_lookup(source_text, 3);

    // // handle.read_to_string(&mut buffer)?;
    handle.read_line(&mut buffer).unwrap();
    println!("{}", buffer);
    let mut result: Vec<String> = vec![];
    for c in buffer.chars() {
        let encoded = encode(c, &lookup);
        result.push(encoded.1);
    }
    println!("{}", result.join(""));
    Ok(())
}

fn create_lookup(source: &str, offset: usize) -> HashMap<String, String> {
    let mut lookup: HashMap<String, String> = HashMap::new();
    let mut letters: Vec<_> = source.split("").collect();
    letters.remove(0);
    letters.remove(letters.len() - 1);
    // println!("{:?}", letters);
    let letters_len = letters.len();
    let start = 0;

    for index in start..letters_len {
        // let index: usize = idx as usize;
        let new_index: usize = (index + offset) % letters_len;
        let key = letters.get(index);
        let value = letters.get(new_index);
        match key {
            Some(k) => match value {
                Some(v) => {
                    lookup.insert(
                        k.to_ascii_uppercase().to_string(),
                        v.to_ascii_uppercase().to_string(),
                    );
                }
                _ => {
                    lookup.insert(NA.to_string(), NA.to_string());
                }
            },
            _ => {
                lookup.insert(NA.to_string(), NA.to_string());
            }
        }

        //     // println!("{}", new_index);
    }
    lookup.insert("offset".to_string(), offset.to_string());
    lookup
}

fn encode(letter: char, lookup: &HashMap<String, String>) -> (String, String) {
    let upper_char = letter.to_ascii_uppercase();
    match lookup.get(&(upper_char.to_string())) {
        Some(value) => {
            return (upper_char.to_string(), value.to_string());
        }
        _ => {
            return (upper_char.to_string(), upper_char.to_string());
        }
    }
}
