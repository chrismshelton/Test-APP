DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
. $DIR/private.sh

rsync -av  $DIR/*.php $SERVER_USER@$SERVER_ADDR:/$APP_ROOT_DIR/
