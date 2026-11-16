use std::fmt;

#[derive(Debug, PartialEq)]
pub enum DurationError {
    Empty,
    MissingNumber(char),
    UnknownUnit(char),
    NoUnit(String),
}

impl fmt::Display for DurationError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self {
            DurationError::Empty => write!(f, "empty duration"),
            DurationError::MissingNumber(unit) => write!(f, "missing number before '{unit}'"),
            DurationError::UnknownUnit(unit) => write!(f, "unknown unit '{unit}'"),
            DurationError::NoUnit(digits) => write!(f, "number without unit: {digits}"),
        }
    }
}

impl std::error::Error for DurationError {}

fn seconds_per(unit: char) -> Result<u64, DurationError> {
    match unit {
        'h' => Ok(3600),
        'm' => Ok(60),
        's' => Ok(1),
        other => Err(DurationError::UnknownUnit(other)),
    }
}

pub fn parse_duration(input: &str) -> Result<u64, DurationError> {
    if input.is_empty() {
        return Err(DurationError::Empty);
    }
    let mut total = 0;
    let mut digits = String::new();
    for c in input.chars() {
        if c.is_ascii_digit() {
            digits.push(c);
            continue;
        }
        let n: u64 = digits.parse().map_err(|_| DurationError::MissingNumber(c))?;
        total += n * seconds_per(c)?;
        digits.clear();
    }
    if !digits.is_empty() {
        return Err(DurationError::NoUnit(digits));
    }
    Ok(total)
}

pub fn total_duration(items: &[&str]) -> Result<u64, DurationError> {
    // Summing an iterator of Results stops at the first Err.
    items.iter().map(|item| parse_duration(item)).sum()
}
