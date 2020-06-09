use std::collections::HashMap;
use std::env;

use std::io::{self, BufRead, Read};

use structopt::clap::AppSettings;
use structopt::StructOpt;

/// Search for a pattern in a file and display the lines that contain it.
#[derive(Debug, StructOpt)]
#[structopt(
    name = "example",
    about = "An example of StructOpt usage.",
    setting = AppSettings::AllowNegativeNumbers
)]
struct Opt {
    // short and long flags (-d, --debug) will be deduced from the field's name
    #[structopt(short, long)]
    debug: bool,
    #[structopt(short = "m", long = "message")]
    message: String,
    /// The path to the file to read
    #[structopt(short = "o", long = "offset", default_value = "3")]
    offset: i8,
}

fn main() -> io::Result<()> {
    // let arg_a = std::env::args().nth(1).expect("no pattern given");
    // let arg_b = std::env::args().nth(2).unwrap_or("".to_string());

    let opt = Opt::from_args();

    let mut buffer = String::new();
    let stdin = io::stdin();
    let mut handle = stdin.lock();
    handle.read_line(&mut buffer).unwrap();
    println!("{}", buffer);
    println!("{}", buffer.get(0..33).unwrap_or("NA"));

    let ans = encode();

    println!("{:?}", ans);
    println!("{:?}", opt);
    Ok(())
}

fn encode() -> (String, String) {
    let opt = Opt::from_args();
    println!("encode {:?}", opt);
    ("A".to_string(), "B".to_string())
}
