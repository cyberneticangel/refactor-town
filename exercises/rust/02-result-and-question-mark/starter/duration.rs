pub fn parse_duration(input: &str) -> Result<u64, String> {
    if input.len() == 0 {
        return Err(String::from("empty duration"));
    }
    let mut total: u64 = 0;
    let mut digits = String::new();
    for c in input.chars() {
        if c.is_ascii_digit() {
            digits.push(c);
            continue;
        }
        let n: u64;
        match digits.parse::<u64>() {
            Ok(v) => {
                n = v;
            }
            Err(_) => {
                return Err(format!("missing number before '{}'", c));
            }
        }
        let mult: u64;
        if c == 'h' {
            mult = 3600;
        } else if c == 'm' {
            mult = 60;
        } else if c == 's' {
            mult = 1;
        } else {
            return Err(format!("unknown unit '{}'", c));
        }
        total = total + n * mult;
        digits = String::new();
    }
    if digits.len() > 0 {
        return Err(format!("number without unit: {}", digits));
    }
    return Ok(total);
}

pub fn total_duration(items: &[&str]) -> Result<u64, String> {
    let mut sum = 0;
    for item in items {
        match parse_duration(item) {
            Ok(v) => sum = sum + v,
            Err(e) => return Err(e),
        }
    }
    Ok(sum)
}
