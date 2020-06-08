use std::collections::HashMap;
use std::io::{self, BufRead};
use unicode_reverse::reverse_grapheme_clusters_in_place;

fn main() -> io::Result<()> {
    let mut buffer = String::new();
    let stdin = io::stdin();
    let mut handle = stdin.lock();

    // handle.read_to_string(&mut buffer)?;
    handle.read_line(&mut buffer).unwrap_or(32);
    println!("{}", buffer);
    reverse_grapheme_clusters_in_place(&mut buffer);
    println!("{}", buffer);

    Ok(())
}
