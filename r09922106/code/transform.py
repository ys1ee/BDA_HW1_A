import json

def transform(input_file, output_file):
    with open(input_file, 'r') as f:
        data = json.load(f)

    new_data = {}
    for i in range(len(data)):
        video_name = data[i]['file_upload'].split('-')[1]
        new_data[video_name] = []
        for res in data[i]['annotations'][0]['result']:
            action = res['value']['sequence']
            action_type = res['value']['labels'][0]
            if action_type == 'click':
                down = [action[0]['x'] + action[0]['width'] / 2, action[0]['y'] + action[0]['height'] / 2]
                up = [action[1]['x'] + action[1]['width'] / 2, action[1]['y'] + action[1]['height'] / 2]
            elif action_type == 'swipe':
                down = [action[0]['x'], action[0]['y'] + action[0]['height']]
                up = [action[1]['x'], action[1]['y']]
            else:
                down = None
                up = None
            new_data[video_name].append({
                'start_frame': str(action[0]['frame']),
                'end_frame': str(action[1]['frame']),
                'action_type': action_type,
                'down_coordinate': down,
                'up_coordinate': up,
                'type_word': None if action_type != 'type' else 'google'
            })
    
    with open(output_file, 'w') as f:
        json.dump(new_data, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    transform('annotation.json', 'annotate.json')