use std::collections::HashMap;
use std::env;
use std::io::{self, BufRead};

fn main() -> io::Result<()> {
    let debug = env::var("DEBUG").is_ok();
    let mut buffer = String::new();
    let stdin = io::stdin();
    let mut handle = stdin.lock();
    let mut encoding_lookup = HashMap::new();

    encoding_lookup.insert(String::from("A"), "*-");
    encoding_lookup.insert(String::from("B"), "-***");
    encoding_lookup.insert(String::from("C"), "-*-*");
    encoding_lookup.insert(String::from("D"), "-**");
    encoding_lookup.insert(String::from("E"), "*");
    encoding_lookup.insert(String::from("F"), "**-*");
    encoding_lookup.insert(String::from("G"), "--*");
    encoding_lookup.insert(String::from("H"), "****");
    encoding_lookup.insert(String::from("I"), "**");
    encoding_lookup.insert(String::from("J"), "*---");
    encoding_lookup.insert(String::from("K"), "-*-");
    encoding_lookup.insert(String::from("L"), "*-**");
    encoding_lookup.insert(String::from("M"), "--");
    encoding_lookup.insert(String::from("N"), "-*");
    encoding_lookup.insert(String::from("O"), "---");
    encoding_lookup.insert(String::from("P"), "*--*");
    encoding_lookup.insert(String::from("Q"), "--*-");
    encoding_lookup.insert(String::from("R"), "*-*");
    encoding_lookup.insert(String::from("S"), "***");
    encoding_lookup.insert(String::from("T"), "-");
    encoding_lookup.insert(String::from("U"), "**-");
    encoding_lookup.insert(String::from("V"), "***-");
    encoding_lookup.insert(String::from("W"), "*--");
    encoding_lookup.insert(String::from("X"), "-**-");
    encoding_lookup.insert(String::from("Y"), "-*---");
    encoding_lookup.insert(String::from("Z"), "--**");
    encoding_lookup.insert(String::from("1"), "*----");
    encoding_lookup.insert(String::from("2"), "**---");
    encoding_lookup.insert(String::from("3"), "***--");
    encoding_lookup.insert(String::from("4"), "****-");
    encoding_lookup.insert(String::from("5"), "*****");
    encoding_lookup.insert(String::from("6"), "-****");
    encoding_lookup.insert(String::from("7"), "--***");
    encoding_lookup.insert(String::from("8"), "---**");
    encoding_lookup.insert(String::from("9"), "----*");
    encoding_lookup.insert(String::from("0"), "-----");

    for (key, value) in &encoding_lookup {
        println!("{}: {}", key, value);
    }

    handle.read_line(&mut buffer).unwrap();
    println!("{}", buffer);
    let mut result: Vec<String> = vec![];
    for c in buffer.chars() {
        let upper_char = c.to_ascii_uppercase();
        let upper_key = upper_char.to_string();
        match encoding_lookup.get(&upper_key) {
            Some(&value) => {
                if debug {
                    println!("{}", value);
                }
                result.push(value.to_string());
            }
            _ => {
                if debug {
                    println!("Key not found '{}'", &upper_key);
                }
                let uk = upper_char.to_string();
                result.push(uk);
                // result.push(" "); // WORKS
            }
        }
    }
    let result_str = result.join(" ");
    println!("'{}'", result_str);
    Ok(())
}
