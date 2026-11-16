mod duration;
use duration::*;

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn parses_valid_durations() {
        assert_eq!(parse_duration("90s"), Ok(90));
        assert_eq!(parse_duration("1h30m"), Ok(5400));
        assert_eq!(parse_duration("2m5s"), Ok(125));
        assert_eq!(parse_duration("1h1h"), Ok(7200));
        assert_eq!(parse_duration("0s"), Ok(0));
    }

    fn err_text(input: &str) -> String {
        parse_duration(input).unwrap_err().to_string()
    }

    #[test]
    fn reports_errors() {
        assert_eq!(err_text(""), "empty duration");
        assert_eq!(err_text("5x"), "unknown unit 'x'");
        assert_eq!(err_text("h"), "missing number before 'h'");
        assert_eq!(err_text("1h30"), "number without unit: 30");
        assert_eq!(err_text("x"), "missing number before 'x'");
    }

    #[test]
    fn totals() {
        assert_eq!(total_duration(&["1m", "30s", "1h"]), Ok(3690));
        assert_eq!(total_duration(&[]), Ok(0));
    }

    #[test]
    fn total_stops_at_first_error() {
        let err = total_duration(&["1m", "oops", "5q"]).unwrap_err();
        assert_eq!(err.to_string(), "missing number before 'o'");
    }
}
