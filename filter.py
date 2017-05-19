import csv
import os
from datetime import datetime
from shutil import rmtree
import traceback
from math import floor
import time

tmp_log = 'instructions.tmp'
csv_path = 'stock.csv'
delimeter = ':::'
super_delimeter = '!!!'

locations = {
    0: "WC",
    1: "BC",
    2: "ND",
    3: "MB"
}

locs = ['WC', 'BC', 'ND', 'MB', 'ALL']

archive = 'archive-log.txt'


chuck = """
                                          MMMMMMMMMMM
                                       MMMMMMMMMMMMMMMMM
                                   NMMMMMMMMMMMMMMMMMMMMMMMM
                                 MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
                                MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMN
                                MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
                               MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
                               MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMD
                              DMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
                              MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
                              MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
                             MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
                             MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
                            MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMN
                            MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMN
                           MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMN
                           MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMN
      NM                  MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
      MMMMM              MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
       MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
        MMMMMMMMMMMMMMMMMMMMMMMMMM8MMMMMMMMMIMMMMM8,. ...........OMMMMMMMMMMMMMMMMMMMMMMMMMMMM
           MMMMMMMMMMMMMMMMMMMMMMM ..N. .....~MMMM...............:MMMMNMMMMMMMMMMMMMMMMMMMMMMM
             NMMMMMMMMMMMMMMMMMMMMM.....:..DMMMMMNZ Z.... .......M$MMMMMMMMMMMMMMMMMMMMMMMMMMM
                 MMMMMMMMMMNMMMMMMM....... 7=MMMMMMO....Z .......MM7MMMMMMMMMMMMMMMMMMMMMMMMM
                    MMMMMMMMMMMMMMMMM  Z...MMMZ .. .,M..,........MMMMMMMMMMMMMMMMMMMMMMMMMMMM
                        MMMMMM.......DOM ....N7..................MMMMMMMMMMMMMMMMMMMMMMMMMMM
                           MMM....... M. ... .  ... ..............M...$MMMMMMMMMMMMMMMMMMMM
                             ........... ........~. ..............M..=....+MMMMMMMMMMMMMM
                             ......+.NMI~........ . ..............M.,.I...MMMMMMMMMMMMMMN
                             ......$... ...... O..................,.....$MMMMMMMMMMMMN
                             .....M.......... M M.. .............. 8  .OMMMMMMMMMMMN
                              ..=7I,,.,,IMI...M.................. ..MMMMMMMMMMM
                              ....DMMMMMMMMMMMMMMMO..............D...MMMMMMMMM
                               .MMMMMMMMMMMMMMDDMM:,N..............DMMMMMMMMMMM
                               NMMMMMNMM8 . .... ...,~............  MMMMMMMMM
                               MMMMM,:......::~..M8M8MM...............MMMMMM
                               MMMM ... . .........,MM..............MMMMMO$
                               MMMMM... =.=. .. . . MM ....... . ...MMMMMMM
                                NMMMMMMMMMM?  ..O.?NM7 ....... ......MMMMMM
                                 NMMMMMMMMMMMMMMMMM........  $ . ...MMMNMMM
                                  MMMMMMMMMMMMMMM.........,, ......MMMMMMMM
                                   OMMMMMMMM8 , .. .. .,N.... ...:MMMMMMMMMMN
                                    MMMMMMMM?N. ...~MD.:MNI8MMMMMMMMMMMMMMMMMN
                               MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMN
                            NMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMN
                           MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMN
                        MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
                     MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
                    NMMMMMMMMMMMMNMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
                   MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
"""


report_names = {
    "WC_to_BC": "WC_to_BC_Pull_List.txt",
    "WC_to_MB": "WC_to_MB_Pull_List.txt",
    "WC_to_ND": "WC_to_ND_Pull_List.txt",
    "BC_to_MB": "BC_to_MB_Pull_List.txt",
    "BC_to_ND": "BC_to_ND_Pull_List.txt",
    "BC_to_WC": "BC_to_WC_Pull_List.txt",
    "MB_to_ND": "MB_to_ND_Pull_List.txt",
    "MB_to_WC": "MB_to_WC_Pull_List.txt",
    "MB_to_BC": "MB_to_BC_Pull_List.txt",
    "ND_to_WC": "ND_to_WC_Pull_List.txt",
    "ND_to_BC": "ND_to_BC_Pull_List.txt",
    "ND_to_MB": "ND_to_MB_Pull_List.txt"
}


def sort_lines(item, line):
    report = report_names.get(line[-10:].rstrip(), 'ERROR.TXT')
    with open("pullsheets/" + report, 'a') as f:
        qty = [str(int(s)) for s in line.split() if s.isdigit()]
        if qty[0] != '0':
            f.write('[ ] ' + item.rstrip() + " Qty: " + qty[0] + "\r\n")


def distribute(*values):
    low = min(values)
    high = max(values)
    if (high - low)**2 <= 1:
        return list(values)
    s = sum(values)
    n = len(values)
    avg = s // n
    result = [avg] * n
    for i in range(s % n):
        result[i] += 1
    return result


def write_to_log(message):
    with open(tmp_log, 'a') as f:
        f.write(message + "\r\n")


def print_move_line(number_to_move, exporter, importer):
    line = "Move " + str(number_to_move) + " from " + locations.get(exporter, "bad location") + "_to_" + locations.get(importer, "bad location")
    write_to_log(line)


def get_steps_for_distribution(have, want):
    # print 'Normal distribution'
    # print 'current: {}, desired {}'.format(have, want)
    for exporter_index in range(0, len(have)):
        diff = have[exporter_index] - want[exporter_index]

        # Move 'diff' units from bin 'exporter_index' to others;
        # offer valid only while supplies last.
        while diff > 0:
            for j in range(1, len(have)):
                # Start next to the exporter and wrap around.
                importer_index = (exporter_index + j) % len(have)
                # print("  DEBUG: have", have, "want", want, "\t", exporter_index, "to", importer_index)
                importer_diff = have[importer_index] - want[importer_index]

                # If this bin needs units, move what we have.
                if importer_diff < 0:
                    number_to_move = min(diff, (-importer_diff))
                    # print("  DEBUG: bin", importer_index, "needs", importer_diff, "donor has", diff)
                    diff -= number_to_move
                    have[exporter_index] -= number_to_move
                    importer_diff -= number_to_move
                    have[importer_index] += number_to_move
                    print_move_line(number_to_move, exporter_index, importer_index)


def pull_all_to_x(location, current_values):
    # Relocate all items to one location
    # print 'pull all inventory to {}'.format(location)
    s = sum(current_values)
    loc = location.upper()
    if loc == 'WC':
        get_steps_for_distribution(current_values, [s, 0, 0, 0])
    elif loc == 'BC':
        get_steps_for_distribution(current_values, [0, s, 0, 0])
    elif loc == 'ND':
        get_steps_for_distribution(current_values, [0, 0, s, 0])
    elif loc == 'MB':
        get_steps_for_distribution(current_values, [0, 0, 0, s])
    elif loc == 'HQ':
        get_steps_for_distribution(current_values, [s, 0, 0, 0])


def pull_all_to_xy(location1, location2, current_values):
    # Handle intentional uneven distributions that
    # are location specific
    # print 'pull all inventory to {}, {}'.format(location1, location2)
    dist = distribute(*[sum(current_values), 0])
    loc1 = location1.upper()
    loc2 = location2.upper()
    locs = [loc1, loc2]
    # print dist, locs, [dist[0], dist[1], 0, 0]
    if 'WC' and 'BC' in locs:
        get_steps_for_distribution(current_values, [dist[0], dist[1], 0, 0])
    elif 'WC' and 'ND' in locs:
        get_steps_for_distribution(current_values, [dist[0], 0, dist[1], 0])
    elif 'WC' and 'MB' in locs:
        get_steps_for_distribution(current_values, [dist[0], 0, 0, dist[1]])
    elif 'BC' and 'ND' in locs:
        get_steps_for_distribution(current_values, [0, dist[0], dist[1], 0])
    elif 'BC' and 'MB' in locs:
        get_steps_for_distribution(current_values, [0, dist[0], 0, dist[1]])
    elif 'MB' and 'ND' in locs:
        get_steps_for_distribution(current_values, [0, 0, dist[0], dist[1]])
    elif 'BC' and 'MB' in locs:
        get_steps_for_distribution(current_values, [0, dist[0], 0, dist[1]])


def pull_all_to_xyz(loc_list, current_values):
    # Handle intentional uneven distributions that
    # are location specific
    # print 'pull all inventory to {}, {}, {}'.format(loc_list[0], loc_list[1], loc_list[2])
    locs = [x.upper() for x in loc_list]

    dist = distribute(*[sum(current_values), 0, 0])
    l = [0]*4
    if 'WC' not in locs:
        get_steps_for_distribution(current_values, [0, dist[0], dist[1], dist[2]])
    elif 'BC' not in locs:
        get_steps_for_distribution(current_values, [dist[0], 0, dist[1], dist[2]])
    elif 'ND' not in locs:
        get_steps_for_distribution(current_values, [dist[0], dist[1], 0, dist[2]])
    elif 'MB' not in locs:
        get_steps_for_distribution(current_values, [dist[0], dist[1], dist[2], 0])


def pull_to_super(item, current):
    for index, i in enumerate(current):
        if i != 0:
            with open('pullsheets/Super_' + locations.get(index, 'ERROR.TXT') + '.txt', 'a') as f:
                f.write('[ ] ' + item + ' Qty: ' + str(i) + '\r\n')


def convert(s):
    # handle messy numbers in inventory
    # that contain negative signs and commas
    # as strings. Convert to whole numbers
    s = s.translate(None, '-,')
    return int(floor(float(s)))


def read_csv(csv_path):
    # Read from csv file
    with open(csv_path, 'rU') as csvfile:
        reader = csv.DictReader(csvfile)
        for index, row in enumerate(reader):
            
            try:
                r = [
                    convert(row['WC Qty']),
                    convert(row['BC Qty']),
                    convert(row['ND Qty']),
                    convert(row['MB Qty'])
                    ]
            except ValueError:
                # print row['Description 1'], 'End of file'
                continue

            desc = row['Description 1']
            control = row['STOCK CONTROL']

            # ! Super sale, move all to ND
            # overrides all other directives
            if '!' in control:
                # print '! - Super Sale: {}'.format(desc)
                # write_to_log(super_delimeter) # change delimeter to make special pull sheet
                # write_to_log("Item: " + desc + "  Alt: " + row['Alternate Lookup'])
                # pull_all_to_x('ND', r)
                pull_to_super("Item: " + desc + "  Alt: " + row['Alternate Lookup'], r)
                continue

            # Ignore for special order or closeout
            elif '#' in control:
                # print '# - Ignore: {}'.format(desc)
                continue

            # # Search for location markers in desc2
            elif len(control) > 0:
                write_to_log(delimeter)
                write_to_log("Item: " + desc + "  Alt: " + row['Alternate Lookup'])
                
                locs_in_control = []
                
                # Grab all valid locations from control
                for loc in locs:
                    if loc in control.upper():
                        locs_in_control.append(loc)
                
                # print 'LOCS IN CONTROL: {}'.format(locs_in_control)
                if 'ALL' in locs_in_control:
                    get_steps_for_distribution(r, distribute(*r))

                elif len(locs_in_control) == 1:
                    pull_all_to_x(locs_in_control[0], r)
                
                elif len(locs_in_control) == 2:
                    pull_all_to_xy(locs_in_control[0], locs_in_control[1], r)

                elif len(locs_in_control) == 3:
                    pull_all_to_xyz(locs_in_control, r)

            # # No special directives, just balance this item
            else:
                # print 'No directives', desc
                write_to_log(delimeter)
                write_to_log("Item: " + desc + "  Alt: " + row['Alternate Lookup'])
                get_steps_for_distribution(r, distribute(*r))


def create_reports():

    for k, v in report_names.iteritems():
        if os.path.exists(v):
            os.remove(v)

    with open(tmp_log, 'r') as f:
        for line in f:
            if delimeter in line:
                continue
            elif "Item" in line:
                item = line.split('Item: ')[1]
            elif "Move" in line:
                sort_lines(item, line)
            else:
                continue

# def archive_pullsheets():
#     '''
#       Archive old versions of pullsheets for continuity checking
#       down the road, should any problems arise we can look back at the
#       pull sheets to see what caused it. Also a potential roll back for
#       inventory locating.
#     '''
#     for i in os.listdir('pullsheets'):
#         if 'archive-log' or 'FOR_ZACK' in i:
#             continue
#         # timestamp this shit
#         with open(archive, 'a') as arch_file:
#             with open(os.path.join('pullsheets/', i), 'r') as i_file:
#                 arch_file.write('test')


def main():
    startTime = datetime.now()

    if os.path.exists(tmp_log):
        os.remove(tmp_log)
    
    if os.path.isdir('pullsheets'):
        # archive_pullsheets()
        rmtree('pullsheets')
    os.makedirs('pullsheets')
    
    read_csv(csv_path)    
    create_reports()
    # os.remove(tmp_log)
    
    with open('pullsheets/FOR_ZACK.TXT', 'a') as f:
        f.write(chuck)

    print "Completed in: {}".format(datetime.now() - startTime)
    

if __name__ == '__main__':
    main()
    # add future tests here