from incident_parser import IncidentCopilot
from datetime import datetime
import sys

def main():
    copilot = IncidentCopilot()
    
    # Read input
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            raw_input = f.read()
    else:
        print("Enter incident notes (press Ctrl+Z then Enter on Windows when done):")
        raw_input = sys.stdin.read()
    
    print("\n🔄 Analyzing incident...\n")
    
    # Parse incident
    report = copilot.parse_incident(raw_input)
    
    # Generate markdown
    markdown = copilot.format_markdown(report)
    
    # Save output
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"output/incident_report_{timestamp}.md"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(markdown)
    
    print(markdown)
    print(f"\n✅ Report saved to: {output_file}")

if __name__ == "__main__":
    main()
