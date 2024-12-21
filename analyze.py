import sys
import re
def parse_perf_output(perf_data):
    tlb_misses = {}
    page_size = 2 * 1024 * 1024  
    with open(perf_data, 'r') as f:
        for line in f:
            if not line or line.startswith("#") or not line.strip():
                continue
            # Split the line into columns based on whitespace
            columns = re.split(r'\s{2,}', line.strip())
           # Extract relevant columns
            tlb_access = columns[9] if len(columns) > 9 else ""
            virtual_address = columns[6] if len(columns) > 6 else ""
            # Clean the virtual address string to remove any unwanted prefixes
            virtual_address_cleaned = re.sub(r'^\[.*?\]\s*', '', virtual_address).strip()
            if 'L2 miss' in tlb_access:
                try:
                    address_int = int(virtual_address_cleaned, 16)  
                    page_address = (address_int // page_size) * page_size  # Calculate the page address 
                    if page_address in tlb_misses:
                        tlb_misses[page_address] += 1  # Increment TLB miss count of the page.
                    else:
                        tlb_misses[page_address] = 1  # Initialize miss count
            
                except (IndexError, ValueError): 
                    continue

    return tlb_misses

def optimal_pages(tlb_misses, n):
    sorted_pages = sorted(tlb_misses.items(), key=lambda item: item[1], reverse=True) #Sort in decreasing order of number of TLB misses.
    return [page[0] for page in sorted_pages[:n]]  # Return the top n pages

def largepages_file(optimal_pages, output_file='largepages.txt'):
    with open(output_file, 'w') as f:
        for page in optimal_pages:
            f.write(f'{page}\n') 

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 analyze.py <n>")
        sys.exit(1)

    n = int(sys.argv[1])  # Number of top pages to find
    perf_data = 'mem_accesses.txt'  # Input file path
    tlb_misses = parse_perf_output(perf_data)  # Parse the performance data
    optimal_pages = optimal_pages(tlb_misses, n)  # Find optimal pages
    largepages_file(optimal_pages)  # Write results to file

    if optimal_pages:
        print(f"Optimal pages written to largepages.txt")
    else:
        print("No optimal pages found. largepages.txt will be empty.")

    
    
