from subprocess import Popen, PIPE
from datetime import datetime
import os, signal, select, time


# Important output
# Block synchronisation started
# Mining operation aborted due to sync operation
# imported 256 block(s) (0 queued 0 ignored) in 2.372852125s. #396572 [7b317a5e / c58170d4]
# Starting mining operation (CPU=0 TOT=1)



class GethMarshal(object):
    # TODO: get the location of the geth binary from config file
    def __init__(self, config):
        self.config = config
        self.gethFile = config['geth-server']

        self.command = [
            self.gethFile,
            '--rpccorsdomain',
            'localhost',
            '--rpc',
            '--autodag'
            # TODO: interface with the javascript console
            #console
        ]

        self.process = None
        self.open = [False, False]
        self.running = False
        self.blockSyncStarted = False
        self.mining = False
        

    def runGeth(self):
        self.process = Popen(self.command, stderr=PIPE, stdout=PIPE)
        self.f = open('gethlog.txt', 'w')
        self.f.write('Geth Log ' + str(datetime.now()) + '\n')
        
        self.open = [True, True]
        self.running = True


    def getOutputLines(self):
        lines = []
        # TODO: check if output is '' from either stream and
        # when both have closed process is dead

        reads = [self.process.stderr.fileno(), self.process.stdout.fileno()]
        ret = select.select(reads, [], [], 0.5)
        if self.process.stderr.fileno() in ret[0]:
            line = self.process.stderr.readline()
            lines.append(self.processLine(line.strip()))
        if self.process.stdout.fileno() in ret[0]:
            line = self.process.stdout.readline()
            lines.append(self.processLine(line.strip()))


        return lines

    def isRunning(self):
        return self.running

    def getOutput(self):
        lines = self.getOutputLines()
        
        retLines = []
        for line in lines:
            try:
                stripped = filter(lambda a: a != '', line.split(' '))
                if self.isStartMiningOperation(stripped):
                    self.mining = True
                    retLines.append(('',' '.join(stripped)))
                elif self.isMiningAbortedLine(stripped):
                    self.mining = False
                    retLines.append(('',' '.join(stripped)))
                elif self.isProtocolVersionLine(stripped):
                	retLines.append(('',' '.join(stripped)))
                elif self.isBlockChainVersionLine(stripped):
                	retLines.append(('',' '.join(stripped)))
                elif self.isStartingServerLine(stripped):
                	retLines.append(('',' '.join(stripped)))
                elif self.isStoppingServerLine(stripped):
                	retLines.append(('',' '.join(stripped)))
                elif self.isDatabaseCloseLine(stripped):
                	retLines.append(('',' '.join(stripped)))
                #elif self.isWaitingForNetworkSyncLine(stripped):
                	#retLines.append(('NETWORKSYNCLINE',' '.join(stripped)))
                    #retLines.append(('', ' '.join(stripped)))
                elif self.isImportingBlocksLine(stripped):
                	pass
                    #retLines.append(('',' '.join(stripped)))
                elif self.isBlockSyncStartedLine(stripped):
                    self.blockSyncStarted = True
                    retLines.append(('',' '.join(stripped)))

                elif self.isBlockchainError(stripped):
                    self.isRunning = False

                elif self.config['verbose'] or self.config['debug']:
                    retLines.append(('', ' '.join(stripped)))
            except IndexError:
                if ' '.join(stripped).strip() != '':
                    retLines.append(('', ' '.join(stripped)))

            self.f.write(line + '\n')
            

        return retLines


    def isStartMiningOperation(self, stripped):
        # Starting mining operation (CPU=0 TOT=1)
        return stripped[0] == 'Starting' and stripped[1] == 'mining' and stripped[2] == 'operation' and self.blockSyncStarted == True and self.mining == False

    def isMiningAbortedLine(self, stripped):
        #  Mining operation aborted
        return stripped[0] == "Mining" and stripped[1] == "operation" and stripped[2] == 'aborted' and self.mining == True

    def isProtocolVersionLine(self, stripped):
    	# Protocol Version: 60, Network Id: 0
    	return stripped[0] == "Protocol" and stripped[1] == "Version:"

    def isBlockChainVersionLine(self, stripped):
        #  Blockchain DB Version: 2
        return stripped[0] == "Blockchain" and stripped[1] == "DB" and stripped[2] == 'Version:'

    def isStartingServerLine(self, stripped):
        #  Starting Server
        return stripped[0] == "Starting" and stripped[1] == "Server"

    def isStoppingServerLine(self, stripped):
        #   Server stopped
        return stripped[0] == "Server" and stripped[1] == "stopped"

    def isDatabaseCloseLine(self, stripped):
        #  flushed and closed db
        return stripped[0] == "flushed" and stripped[1] == "and" and stripped[2] == "closed"

    def isWaitingForNetworkSyncLine(self, stripped):
        #  Can not start mining operation due to network sync (starts when finished)
        return stripped[0] == "Can" and stripped[1] == "not" and stripped[2] == "start"

    def isImportingBlocksLine(self, stripped):
        #  imported 256 block(s)
        return stripped[0] == "imported" and stripped[2] == "block(s)"

    def isBlockSyncStartedLine(self, stripped):
        #  Block synchronisation started
        return stripped[0] == "Block" and stripped[1] == "synchronisation" and stripped[2] == "started"

    def isBlockchainError(self, stripped):
        return stripped[1] == "blockchain" and stripped[2] == "db" and stripped[3] == "err:"
        

    def killGeth(self):
        if self.process is not None:
            self.f.close()
            self.process.kill()
            self.process.wait()
        

    def processLine(self, line):
        return line[line.find(']')+2:]
                





if __name__ == '__main__':
    config = {
        'geth-server': "/home/cameron/go-ethereum/build/bin/geth",
        'verbose': False,
        'debug': False
    }
    gm = GethMarshal(config)
    try:
        gm.runGeth()
        time.sleep(1)
        while gm.isRunning():
            linearray = gm.getOutput()
            for line in linearray:
                print line
    except KeyboardInterrupt:
        print 'Received interrupt, stopping geth...'
        gm.killGeth()


    



